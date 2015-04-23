import os
import cv2
import sys

old_class = 0
truth = 0
w_file = open(sys.argv[1], 'w')
b_file = open(sys.argv[2], 'w')
m_file = open(sys.argv[3], 'w')
with open('test.txt') as f:
	for line in f:
		fields = line.split(' ')
		truth = int(fields[1])
		if truth == 0:
			print fields[0]
			img  = cv2.imread(fields[0])
			cv2.imshow('img',img)
			k = cv2.waitKey()
			if k == 1048624:
				old_class = 0
			elif k == 1048625:		
				old_class = 1
			elif k == 1048626:		
				old_class = 2
			elif k == 1048627:		
				old_class = 3
			elif k == 1048603:
				print "Exiting!"
				w_file.close()
				b_file.close()
				m_file.close()
				quit()		
			else:
				print 'No class selected: ' + str(k)
			if old_class == 0:
				w_file.write("%s %d\n" % (fields[0], truth))
			elif old_class == 1:
				b_file.write("%s %d\n" % (fields[0], truth))
			elif old_class == 2:
				m_file.write("%s %d\n" % (fields[0], truth))

w_file.close()
b_file.close()
m_file.close()
