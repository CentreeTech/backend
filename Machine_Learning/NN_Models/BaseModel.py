
import abc
import random
import requests
import io
import librosa
import soundfile as sf

import boto3
import boto
import boto.s3
import botocore
import numpy as np
import tensorflow as tf
from boto.s3.key import Key
from botocore.client import Config
from io import BytesIO



class BaseModel():

	def __init__(self, classifications, model_info, s3_login_info):
		self.classifications = classifications
		self.counter = 0
		self.num_samples = len(classifications)
		self.batch_size = 20
		self.model_info = model_info
		self.s3_login_info = s3_login_info
		self.hm_epochs = 5

		self.HOP_LENGTH = 50
		self.SAMPLE_RATE = 22050

		self.s3 = boto3.resource(
			's3',
			aws_access_key_id=s3_login_info["AWS_ACCESS_KEY_ID"],
			aws_secret_access_key=s3_login_info["AWS_SECRET_ACCESS_KEY"],
			config=Config(signature_version='s3v4')
		)

		self.num_classes = len(self.model_info["positive_cases"])

		self.features = None
		self.trueOutput = tf.placeholder(tf.float32,[None, self.num_classes], name='trueOutput')

	@abc.abstractmethod
	def build(self):
		return None

	def train(self):
		#model = self.build(self.model_info)

		prediction = self.build()
		cost = tf.reduce_mean(tf.square(tf.subtract(prediction, self.trueOutput)))
		optimizer = tf.train.AdamOptimizer().minimize(cost)

		with tf.Session() as sess:
			sess.run(tf.global_variables_initializer())

			for epoch in range(self.hm_epochs):
				self.reset_batch_counter()
				random.shuffle(self.classifications) #shuffle per epoch to reduce issue of order bias
				epoch_loss = 0
				sessOutput = np.zeros([self.num_samples, self.num_classes])
				while not self.isDone():
					batch = self.get_batch() #this is the set of classifications we're currently going through.
					label_batch, data_batch = self.get_labels_and_data(batch)
					batch_size = len(data_batch)

					data_batch = self.get_features(data_batch)
					print ("FEATURES")
					print (data_batch)

					_, batchLoss, batchOutput = sess.run([optimizer, cost, prediction], 
										feed_dict = {self.features: data_batch, self.trueOutput: label_batch})
					epoch_loss += batchLoss
					sessOutput[batchInd:batchInd+BATCH_SIZE]=batchOutput
			correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(self.trueOutput,1))
			accuracy = tf.reduce_mean(tf.cast(correct,'float'))
			#print ( 'accuracy: ', accuracy.eval({self.features: batchstuff, self.trueOutput: labels}) )

	def isDone(self):
		return self.counter == self.num_samples

	def reset_batch_counter(self):
		self.counter = 0

	def get_batch(self):
		b_size = self.batch_size

		if self.counter < 0:
			print("[Error] Counter is below zero.")
		elif self.counter > self.num_samples:
			print("[Error] Counter is greater than total number of classifications.")
			return None
		elif self.counter + self.num_samples > self.num_samples:
			b_size = self.num_samples - self.counter

		#now we're sure that the counter is good.

		batch = self.classifications[self.counter:self.counter+b_size]
		self.counter += b_size
		return batch

	def get_labels_and_data(self, batch):
		label_batch = []
		filenames = []
		data_batch = []

		for classification in batch:
			onehot = [x==classification["service"] for x in self.model_info["positive_cases"]]
			
			fileName = classification["media"]
			if fileName in filenames:
				data = data_batch[filenames.index(fileName)]
			else:
				print ("about to get file data")
				data = self.get_file_data(fileName)
				print(data)
			if data is not None:
				data_batch += [data]
				label_batch += [onehot]
				filenames += [fileName]
				print (">>entry data acquired!!")
			else:
				print ("File didn't exist!")

		return (np.array(label_batch, dtype = np.int), data_batch)


	def get_features(self, data_batch):
		_features = []
		for time_series in data_batch:
			spectro = librosa.feature.melspectrogram(y = time_series, sr = self.SAMPLE_RATE, hop_length = self.HOP_LENGTH)
			_features += [spectro]

		return _features

	def get_file_data(self, fileName):

		audio_wav = None

		try:
			# audio_wav = io.BytesIO()
			# self.s3.download_fileobj(self.s3_login_info["BUCKET_NAME"], fileName, audio_wav)
			# audio_wav = np.fromstring(audio_wav, dtype=np.int16)
			obj = self.s3.Object(
				bucket_name=self.s3_login_info["BUCKET_NAME"],
				key=fileName
			)
			audio_wav = io.BytesIO(obj.get()["Body"].read())
			data, sample_rate = sf.read(audio_wav, dtype = 'float32')
			data = librosa.resample(data.T, sample_rate, self.SAMPLE_RATE)
			data = librosa.to_mono(data)
			return data

		except botocore.exceptions.ClientError as e:
			if e.response['Error']['Code'] == "404":
				print("The object does not exist.")

			else:
				raise
		return None

	def export(self):
		return None

	def __repr__(self):
		return '<NN Model | name := {}'.format(self.__name__)
