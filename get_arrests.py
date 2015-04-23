from grab import Grab
import sys
import subprocess
import re
import itertools

path = 'http://mugshots.com/US-Counties/North-Carolina/Alamance-County-NC/?page='

while True:
	try:
		g = Grab()
	except:
		continue
	break

first_names=[]
last_names=[]
dates=[]
imgs=[]
results=[]
#&searchDOB=10/14/1988&
g.go(sys.argv[1] + "?page=" + sys.argv[2])
for elem in g.doc.select('//tr/td/a'):
	print elem.attr('href')
	results.append(elem.attr('href'))

for a in results:
	g.go(a)
	i = 0
	tmp = g.doc.select('//h1[@id="item-title"]/span[@itemprop="name"]')
	fields = tmp[0].text().split(' ')
	first_name = fields[0]
	last_name = fields[-1]
	for elem in g.doc.select('//div[@class="fieldvalues"]/div[@class="field"]/span[@class="value"]'):
		if i == 1:
			races = elem.text()
		elif i == 2:
			gender = elem.text()
		elif i == 7:
			date = elem.text()
		i = i + 1

	dates.append(date)
	last_names.append(last_name)
	first_names.append(first_name)
	print date
	fields = date.split('/')
	
	img=""
	i = 0
	for elem in g.doc.select('//div[@class="full-image-container"]/div[@class="full-image"]/img[@class="hidden-wide"]'):
		img_name = first_name + '_' + last_name + '_' + fields[0] + '_' + fields[1] + '_' + fields[2] + '.jpg'
		if i > 0:
			img+=','
		img+=img_name
		server=subprocess.Popen(["wget", '--quiet', '-O', img_name, elem.attr('src') ], cwd='data')
		#print '%s %s %s %s' % (fields[1].split(' ')[1], fields[0], date.text(), img.attr('src'))
	imgs.append(img)

output_file = open(sys.argv[3],'w')
#We have the name and image, now lets get the conviction status
for f,l,d,i, in itertools.izip(first_names,last_names,dates,imgs):
	lookup = 'http://webapps6.doc.state.nc.us/opi/offendersearch.do?method=list&searchLastName=' + l + '&searchFirstName=' + f + '&searchDOB=' + d
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
