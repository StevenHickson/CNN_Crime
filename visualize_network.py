import numpy as np
import matplotlib.pyplot as plt
#from pylab import *
import cv2
import sys

caffe_root = '/home/steve/Documents/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'

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
    
    plt.imshow(data)
    plt.show()
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

input_image = caffe.io.load_image(sys.argv[1])
net.blobs['data'].reshape(1,3,227,227)
net.blobs['data'].data[...] = transformer.preprocess('data', input_image)
#net.blobs['data'].data[...] = input_image
out = net.forward()
#scores = net.predict([input_image])
print("Predicted class is #{}.".format(out['prob'].argmax()))
#print("Predicted class is #{}.".format(scores[0].argmax()))
[(k, v.data.shape) for k, v in net.blobs.items()]
plt.imshow(input_image)
plt.show()
print 'conv1'
filters = net.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1), 'conv1.png')
print 'feat1'
feat = net.blobs['conv1'].data[0, :36]
vis_square(feat, 'feat1.png', padval=1)
print 'conv2'
filters = net.params['conv2'][0].data
vis_square(filters[:48].reshape(48**2, 5, 5), 'conv2.png')
print 'feat2'
feat = net.blobs['conv2'].data[0, :36]
vis_square(feat, 'feat2.png', padval=1)
print 'feat3'
feat = net.blobs['conv3'].data[0]
vis_square(feat, 'conv3.png', padval=0.5)
print 'feat4'
feat = net.blobs['conv4'].data[0]
vis_square(feat, 'conv4.png', padval=0.5)
print 'feat5'
feat = net.blobs['conv5'].data[0]
vis_square(feat, 'conv5.png', padval=0.5)
print 'pool5'
feat = net.blobs['pool5'].data[0]
vis_square(feat, 'pool5.png', padval=1)
