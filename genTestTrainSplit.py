from collections import defaultdict
import sys
import random
import os.path

d = defaultdict(list)
train_file = open(sys.argv[2],'w')
test_file = open(sys.argv[3],'w')

with open(sys.argv[1]) as f:
	for line in f:
		#parse line here
		fields = line.split(',')
		newString = fields[2] + ',' + fields[3].rstrip('\r\n')
		d[int(fields[3])].append(newString)

#Lets parse out keys with a small list and split the rest 80/20
for k,v in d.items():
	#We only care about things with more than 20 examples
	if len(v) >= 0:
		#Lets print the keys for posterity
		print "%s" % (str(k))
		random.shuffle(v)
		train_i = int(len(v)*0.8)
		train_data = v[:train_i]
		test_data = v[train_i:]

		#lets output the filenames to test and train
		for item in train_data:
			fields = item.split(',')
			full = '/home/steve/inmates/data/' + fields[0]
			if os.path.isfile(full):
				train_file.write("%s %d\n" % (full, int(fields[1])))
		for item in test_data:
			fields = item.split(',')
			full = '/home/steve/inmates/data/' + fields[0]
			if os.path.isfile(full):
				test_file.write("%s %d\n" % (full, int(fields[1])))

train_file.close()
test_file.close()
