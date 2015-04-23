import numpy as np
import matplotlib.pyplot as plt
import sklearn
import sklearn.metrics
from sklearn.metrics import confusion_matrix
import itertools

caffe_root = '/home/steve/Documents/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE = './deploy.prototxt'
PRETRAINED = './models/_iter_80000.caffemodel'
#IMAGE_FILE = '/home/steve/EdisonData/data/dYOSze18voxUwc5292z62i9eM2DfNiFH.jpg'
TEST_FILE = sys.argv[1]

net = caffe.Classifier(MODEL_FILE, PRETRAINED)
net.set_raw_scale('data',255)
net.set_channel_swap('data',(2,1,0))
net.set_mean('data',np.load(caffe_root+'python/caffe/imagenet/ilsvrc_2012_mean.npy'))
#net.set_phase_test()
caffe.set_mode_gpu()

#input_image = caffe.io.load_image(IMAGE_FILE)
#plt.imshow(input_image)
#print 'prediction shape:', prediction[0].shape
#plt.plot(prediction[0])
#print 'predicted class:', prediction[0].argmax()
#plt.show()

pred=[]
truth=[]
probs=[]
with open(TEST_FILE) as f:
	for line in f:
		fields = line.split(' ')
		truth.append(int(fields[1]))
		input_image = caffe.io.load_image(fields[0])
		prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
		pred.append(int(prediction[0].argmax()))
		probs.append(prediction[0])
		#print 'Truth:',fields[1],'Prediction',prediction[0].argmax()

conf=confusion_matrix(truth,pred)
#save output
output_file = open(sys.argv[2],'w')
probs_file = open(sys.argv[3],'w')
for p,a,t in itertools.izip(pred,probs,truth):
	output_file.write("%s,%s\n" % (p, t))
	for e in a:
		probs_file.write("%s " % e)
	probs_file.write("\n")
output_file.close()
probs_file.close()
print conf
positive=0.0
positives=[0] * len(conf)
total=0.0
totals=[0] * len(conf)
for i in range(len(conf)):
    for j in range(len(conf[i])):
	if i == j:
		positive = positive + conf[i][j]
		positives[i] = conf[i][j]
	total = total + conf[i][j]
	totals[i] = totals[i] + conf[i][j]
print positives
print totals
print 'Total Accuracy: ', (positive / total)
classAcc=0.0
print 'Class Accuracies:'
for p,t in itertools.izip(positives,totals):
	if float(t) > 0:
		acc = (float(p) / float(t))
		print 'Accuracy: ', acc
		classAcc = classAcc + acc
	else:
		print 'Accuracy: NaN'
classAcc = classAcc / len(conf[0])
