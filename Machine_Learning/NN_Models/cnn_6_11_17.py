import tensorflow as tf
import numpy as np
import os
import librosa
import sys
import utility as ut
import trainer as tr

print 'BEGINNING MODEL GENERATION.'

#set up this so that we can double check,
#idk I might get rid of it but it looks 
#like it might be useful at some point.
def is_good_feature_dict(nn_hyp_par):
	return True #TODO


def convolutional_neural_net(nn_hyp_par, data):

	fc_width = nn_hyp_par['data_width']
	fc_height = nn_hyp_par['data_height']
	fc_width_by_height = fc_width * fc_height

	fc_input_size = (fc_width_by_height / 4) * 128

	weights = {'conv1' : tf.Variable(tf.random_normal([5,5,1,32])),
			   'conv2' : tf.Variable(tf.random_normal([5,5,32,64])),
			   'conv3' : tf.Variable(tf.random_normal([5,5,64,128])),
			   'fc' : tf.Variable(tf.random_normal([ fc_input_size,1024])),
			   'out' : tf.Variable(tf.random_normal([1024,nn_hyp_par['num_classes']]))}

	biases = {'conv1' : tf.Variable(tf.random_normal([32])),
			   'conv2' : tf.Variable(tf.random_normal([64])),
			   'conv3' : tf.Variable(tf.random_normal([128])),
			   'fc' : tf.Variable(tf.random_normal([1024])),
			   'out' : tf.Variable(tf.random_normal([nn_hyp_par['num_classes']]))}

	data = tf.reshape(data, shape=[-1,nn_hyp_par['data_width'],nn_hyp_par['data_height'],1])

	conv1 = tf.nn.relu( ut.conv2d(data, weights['conv1'])+biases['conv1'] )
	conv1 = ut.maxpool2d(conv1)

	conv2 = tf.nn.relu( ut.conv2d(conv1, weights['conv2'])+biases['conv2'] )
	conv3 = tf.nn.relu( ut.conv2d(conv2, weights['conv3'])+biases['conv3'] )
	#conv2 = ut.maxpool2d(conv2)

	fc = tf.reshape(conv3,[-1, fc_input_size])
	fc = tf.nn.relu(tf.matmul(fc, weights['fc']) + biases['fc'])

	output = tf.sigmoid( tf.matmul(fc, weights['out']) + biases['out'] )

	return output

		# meta_graph_def = tf.train.export_meta_graph(
  #  							 filename='/tmp/my-model.meta',
  #  							 collection_list=["input_tensor", "output_tensor"])


if __name__ == '__main__':
	print 'Beginning to build neural network.'
	nn_hyp_par = {}  #this is a dictionary of hyper parameters for the neural network. 
	nn_hyp_par['data_width'] = 94
	nn_hyp_par['data_height'] = 128
	nn_hyp_par['num_classes'] = 2
	nn_hyp_par['classes'] = { 'male' : [1,0], 'female' : [0,1]}
	nn_hyp_par['dataset_size'] = 40
	nn_hyp_par['batch_size'] = 20
	nn_hyp_par['dataset_dir'] = 'training'
	nn_hyp_par['hm_epochs'] = 1

	x = tf.placeholder('float', [None, nn_hyp_par['data_height'], nn_hyp_par['data_width']], name = "features")
	y = tf.placeholder('float', name = "true_outputs")

	tr.train_neural_net(x, y, nn_hyp_par, convolutional_neural_net)
