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
g.go(path + '/?page=1&results=1000')
for elem in g.doc.select('//ul/li/div/div[@class="title"]/a'):
	#print elem
        #print '%s %s' % (elem.text(), elem.attr('href'))
	names = re.findall('[A-Z][^A-Z]*', elem.text())
	#print '%s %s' % (names[0], names[1])
	if len(names) == 2:
		first_names.append(names[0].split(' ')[0])
		last_names.append(names[1].split(' ')[0])
		records.append(elem.attr('href'))

imgs=[]
for href in records:
	g.go(path + href)
	for elem in g.doc.select('//div/div[@class="picture"]/a/img'):
		mug = elem.attr('src')
		img = mug.split('/')[-1]
		#print '%s %s' % (mug, img)
		server=subprocess.Popen(["wget", '--quiet', path + mug], cwd='data')
		imgs.append(img)

output_file = open('arrests.txt','w')
#We have the name and image, now lets get the conviction status
for f,l,i, in itertools.izip(first_names,last_names,imgs):
	lookup = 'http://webapps6.doc.state.nc.us/opi/offendersearch.do?method=list&searchLastName=' + l + '&searchFirstName=' + f
	#print lookup
	print '%s %s' % (f, l)
	g.go(lookup)
	if g.doc.text_search(u'Nothing found'):
		status=0
	else:
		elem = g.doc.select('//tr/td[@class="tablelink"]/a')
		#print '%s' % elem[0].attr('href')
		g.go('http://webapps6.doc.state.nc.us/opi/' + elem[0].attr('href'))
		if g.doc.text_search(u'INMATE'):
			status=2
		elif g.doc.text_search(u'PROBATION'):
			status=1
		else:
			status=0
	output_file.write("%s,%s,%s,%d\n" % (f,l,i,status))

output_file.close()
server.wait()
