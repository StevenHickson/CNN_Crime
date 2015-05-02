from collections import defaultdict
import sys
import random
import os.path

d = defaultdict(list)
train_file = open(sys.argv[2],'w')
test_file = open(sys.argv[3],'w')
train_full_file = open(sys.argv[4],'w')
test_full_file = open(sys.argv[5],'w')

with open(sys.argv[1]) as f:
	for line in f:
		#parse line here
		fields = line.split(',')
		newString = fields[5] + ',' + fields[7].rstrip('\r\n')
		d[int(fields[7])].append(line)

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
			train_file.write("%s %d\n" % (fields[5], int(fields[7])))
			train_full_file.write("%s" % (item))
		for item in test_data:
			fields = item.split(',')
			test_file.write("%s %d\n" % (fields[5], int(fields[7])))
			test_full_file.write("%s" % (item))
train_file.close()
test_file.close()
