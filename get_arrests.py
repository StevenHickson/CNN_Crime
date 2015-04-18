from grab import Grab
import sys
import subprocess
import re
import itertools

path = 'http://northcarolina.arrests.org'

g = Grab()

first_names=[]
last_names=[]
records=[]
g.go(path + '/?page=1&results=10')
for elem in g.doc.select('//ul/li/div/div[@class="title"]/a'):
	#print elem
        #print '%s %s' % (elem.text(), elem.attr('href'))
	names = re.findall('[A-Z][^A-Z]*', elem.text())
	#print '%s %s' % (names[0], names[1])
	first_names.append(names[0])
	last_names.append(names[1])
	records.append(elem.attr('href'))

imgs=[]
for href in records:
	g.go(path + href)
	for elem in g.doc.select('//div/div[@class="picture"]/a/img'):
		mug = elem.attr('src')
		img = mug.split('/')[-1]
		#print '%s %s' % (mug, img)
		subprocess.Popen(["wget", path + mug], cwd='data')
		imgs.append(img)

#We have the name and image, now lets get the conviction status
