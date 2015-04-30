import numpy as np
import cv2
import sys
import itertools

caffe_root = '/home/steve/Documents/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data, fileName, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    #savefig(fileName)
    #cv2.imwrite(fileName,data.astype(np.uint8))

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = './deploy.prototxt'
PRETRAINED = './models/_iter_80000.caffemodel'

#print dir(caffe)
#print dir(caffe.io)

net = caffe.Classifier(MODEL_FILE, PRETRAINED)
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data', np.load(caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # mean pixel
transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB
#net.set_phase_test()
#net.set_raw_scale('data',255)
#net.set_channel_swap('data',(2,1,0))
#net.set_mean('data',np.load(caffe_root+'python/caffe/imagenet/ilsvrc_2012_mean.npy'))

truth=[]
probs=[]
with open(sys.argv[1]) as f:
	for line in f:
		fields = line.split(' ')
		truth.append(int(fields[1]))
		input_image = caffe.io.load_image(fields[0])
		net.blobs['data'].reshape(1,3,227,227)
		net.blobs['data'].data[...] = transformer.preprocess('data', input_image)
		#net.blobs['data'].data[...] = input_image
		out = net.forward()
		feat = net.blobs['fc7'].data[0]
		#print feat
		probs.append(feat)

output = open(sys.argv[2], 'w')

for prob, label in itertools.izip(probs,truth):
	for a in prob:
		output.write("%f," % a)
	output.write("%d\n" % label)

output.close()
