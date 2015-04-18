from grab import Grab
import sys
import subprocess
import re
import itertools

path = 'http://mugshots.wbtv.com/records/'

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
#&searchDOB=10/14/1988&
g.go(path + sys.argv[1])
query1 = g.doc.select('//div[@id="perps"]/div[@class="perp"]/div[@class="image"]/a/img')
query2 = g.doc.select('//div[@id="perps"]/div[@class="perp"]/div[@class="arrest_date"]/b')
query3 = g.doc.select('//div[@id="perps"]/div[@class="perp"]/div[@class="name"]')
for img,date,name in itertools.izip(query1, query2, query3):
	dates.append(date.text())
	fields = name.text().split(',')
	last_name = fields[0]
	first_name = fields[1].split(' ')[1]
	last_names.append(last_name)
	first_names.append(first_name)
	url = img.attr('src')
	fields = date.text().split('/')
	img_name = first_name + '_' + last_name + '_' + fields[0] + '_' + fields[1] + '_' + fields[2] + '.jpg'
	imgs.append(img_name)
	server=subprocess.Popen(["wget", '--quiet', '-O', img_name, url ], cwd='data')
	#print '%s %s %s %s' % (fields[1].split(' ')[1], fields[0], date.text(), img.attr('src'))

output_file = open(sys.argv[2],'w')
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
