from NN_Models.BaseModel import BaseModel
import tensorflow as tf
import numpy as np
import os
import librosa
import sys

class cnn_neural_net_v1_0(BaseModel):

	def __init__(self, classifications, model_info, s3_login_info):
		super(cnn_neural_net_v1_0, self).__init__(classifications, model_info, s3_login_info)
		self.features = tf.placeholder(tf.float32,[None, 128, 1765, 1], name='features')
		self.neurons_layer_1 = 50
		self.neurons_layer_2 = 50
		self.neurons_layer_3 = 50
		self.input_layer_size = 1765
		self.NUM_CLASSES = 1

	def build(self):

		weights = {'w_conv1' : tf.Variable(tf.random_normal([5,5,1,32])),
			   'w_conv2' : tf.Variable(tf.random_normal([5,5,32,64])),
			   'w_fc' : tf.Variable(tf.random_normal([7*7*64,1024])),
			   'out' : tf.Variable(tf.random_normal([1024,self.NUM_CLASSES]))}
		biases = {'w_conv1' : tf.Variable(tf.random_normal([32])),
			   'w_conv2' : tf.Variable(tf.random_normal([64])),
			   'w_fc' : tf.Variable(tf.random_normal([1024])),
			   'out' : tf.Variable(tf.random_normal([1024,self.NUM_CLASSES]))}

		conv1 = tf.nn.relu( ut.conv2d(self.features, weights['conv1'])+biases['conv1'] )
		conv2 = tf.nn.relu( ut.conv2d(conv1, weights['conv2'])+biases['conv2'] )
		conv3 = tf.nn.relu( ut.conv2d(conv2, weights['conv3'])+biases['conv3'] )
		#conv2 = ut.maxpool2d(conv2)

		fc = tf.reshape(conv3,[-1, fc_input_size])
		fc = tf.nn.relu(tf.matmul(fc, weights['fc']) + biases['fc'])

		return output

	def get_features(self, data_batch):
		_features = []
		for time_series in data_batch:
			spectro = librosa.feature.melspectrogram(y = time_series, sr = self.SAMPLE_RATE, hop_length = self.HOP_LENGTH)
			_features += [spectro]

		return _features