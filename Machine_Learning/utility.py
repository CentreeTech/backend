import tensorflow as tf
import numpy as np
import os
import librosa
import sys


TARGET_SAMPLE_RATE = 16000
TARGET_LEN_SECS = 3
TIME_SERIES_LEN = TARGET_SAMPLE_RATE * TARGET_LEN_SECS

def conv2d(data,w):
	return tf.nn.conv2d(data,w, strides=[1,1,1,1], padding='SAME')

def maxpool2d(data):
	return tf.nn.max_pool(data, ksize = [1,2,2,1], strides=[1,2,2,1], padding='SAME')

def print_progress(iteration, total, prefix='', suffix='', decimals=1, bar_length=50):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = '#' * filled_length + '-' * (bar_length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


#yeah this is a TODO
def loadfile_time_series(folder, startIndex, limit):
    return 1


def loadFile_spectro(folder, startIndex, limit, verbose = False):
    data = []
    index = startIndex
    path = folder+'/'+str(index)+'.flac'
    while(os.path.exists(path) and index < limit):
        #iterating through
        time_series, sample_rate = librosa.load(path)

        if sample_rate != TARGET_SAMPLE_RATE:
            #we need to reset sample rate.
            if sample_rate < TARGET_SAMPLE_RATE:
                #there's nothing we can really do, we just can continue
                continue
            else:
                #then we should reduce the sample rate.
                librosa.core.resample(time_series, sample_rate, TARGET_SAMPLE_RATE)

        if len(time_series) > TIME_SERIES_LEN:
            #then this needs to be trimmed down.
            time_series = time_series[:TIME_SERIES_LEN]
        elif len(time_series) < TIME_SERIES_LEN:
            time_series = librosa.util.fix_length(time_series, TIME_SERIES_LEN)

        spectro = librosa.feature.melspectrogram(y = time_series, sr = sample_rate)

        data += [spectro]
        #print(str(index),spectro)
        if verbose: print_progress(index - startIndex, limit - startIndex, prefix = 'Progress:', suffix = 'Completed | length: ' + str(len(spectro[0])), bar_length = 15)
        index += 1
        path = folder+'/'+str(index)+'.flac'
    if verbose: print
    return data

def loadLabels(fileName):
    csvFile=open(fileName)
    lines=csvFile.read().splitlines()
    csvFile.close()
    splitLines=[]
    for line in lines:
        splitLines+=[line.split('|')]
    return splitLines



