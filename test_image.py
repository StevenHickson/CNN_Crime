import numpy as np
import matplotlib.pyplot as plt
import sys

caffe_root = '/home/steve/Documents/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = './deploy.prototxt'
PRETRAINED = './models/_iter_60000.caffemodel'

net = caffe.Classifier(MODEL_FILE, PRETRAINED)
net.set_raw_scale('data',255)
net.set_channel_swap('data',(2,1,0))
net.set_mean('data',np.load(caffe_root+'python/caffe/imagenet/ilsvrc_2012_mean.npy'))
#net.set_phase_test()

input_image = caffe.io.load_image(sys.argv[1])
plt.imshow(input_image)
plt.show()
prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
print 'prediction shape:', prediction[0].shape
plt.plot(prediction[0])
print 'predicted class:', prediction[0].argmax()
plt.show()
