
import tensorflow as tf
import numpy as np

import utility as ut

def train_neural_net(features, trueOutput, nn_hyp_par, model):
	prediction = model(nn_hyp_par, features)
	cost = tf.reduce_mean(tf.square(tf.subtract(prediction, trueOutput)))

	# 									learningRate = 0.001
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		labels = ut.loadLabels('training/labels.txt')

		for i in range(0,len(labels)):
			if labels[i][1] == 'F':
				labels[i] = nn_hyp_par['classes']['female']
			else:
				labels[i] = nn_hyp_par['classes']['male']
		for epoch in range(nn_hyp_par['hm_epochs']):
			shuffle = np.random.permutation(nn_hyp_par['dataset_size'])
			epoch_loss = 0
			sessOutput = np.zeros([nn_hyp_par['dataset_size'], nn_hyp_par['num_classes']])
			num_batches_per_epoch = nn_hyp_par['dataset_size'] / nn_hyp_par['batch_size']
			total_num_batches = num_batches_per_epoch * nn_hyp_par['hm_epochs']
			for batchInd in range(0, nn_hyp_par['dataset_size'], nn_hyp_par['batch_size']):
				
				#get that batch of data.
				batch_data = ut.loadFile_spectro(nn_hyp_par['dataset_dir'], batchInd, batchInd + nn_hyp_par['batch_size'])
				batch_labels = labels[batchInd:batchInd+nn_hyp_par['batch_size']]
				print(np.shape(batch_data), np.shape(batch_labels))
				_, batchLoss, batchOutput = sess.run([optimizer, cost, prediction], 
										feed_dict = {features: batch_data, trueOutput: batch_labels})
				epoch_loss += batchLoss
				sessOutput[batchInd:batchInd+nn_hyp_par['batch_size']]=batchOutput
				ut.print_progress(epoch * num_batches_per_epoch + (batchInd / nn_hyp_par['batch_size']), total_num_batches, prefix = 'Progress:', suffix = 'Completed | Epoch ' + str(epoch) + ' train loss ' 
	        													+ str(epoch_loss/nn_hyp_par['dataset_size']/nn_hyp_par['batch_size']), bar_length = 15)
		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(trueOutput,1))
		accuracy = tf.reduce_mean(tf.cast(correct,'float'))
		print
		batch_data = ut.loadFile_spectro(nn_hyp_par['dataset_dir'], 0, nn_hyp_par['batch_size'])
		print 'accuracy: ', accuracy.eval({features: batch_data, trueOutput: labels[0:nn_hyp_par['batch_size']]})
		_, batchLoss, batchOutput = sess.run([optimizer, cost, prediction], 
										feed_dict = {features: batch_data, trueOutput: labels[0:nn_hyp_par['batch_size']]})
		print 'values: ', np.round(batchOutput, decimals = 3)
		print 'true values: ', np.round(labels[0:nn_hyp_par['batch_size']], decimals = 3)
		meta_graph_def = tf.train.export_meta_graph(filename='/tmp/my-model.meta')