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
genders=[]
races=[]
dates=[]
imgs=[]
results=[]
#&searchDOB=10/14/1988&
g.go(sys.argv[1] + "?page=" + sys.argv[2])
for elem in g.doc.select('//tr/td/a'):
	results.append(elem.attr('href'))

for a in results:
	g.go(a)
	grab = 0
	tmp = g.doc.select('//h1[@id="item-title"]/span[@itemprop="name"]')
	fields = tmp[0].text().split(' ')
	first_name = fields[0]
	last_name = fields[-1]
	for elem in g.doc.select('//div[@class="fieldvalues"]/div[@class="field"]/span'):
		if grab == 1:
			race = elem.text()
			grab = 0
		elif grab == 2:
			gender = elem.text()
			grab = 0
		elif grab == 3:
			date = elem.text()
			grab = 0
		if elem.text() == "Gender":
			grab = 2
		elif elem.text() == "Race":
			grab = 1
		elif elem.text().split(' ')[0] == "Birth":
			grab = 3
	dates.append(date)
	last_names.append(last_name)
	first_names.append(first_name)
	genders.append(gender)
	races.append(race)
	fields = date.split('/')
	
	elem = g.doc.select('//div[@class="full-image-container"]/div[@class="full-image"]/img[@class="hidden-wide"]')
	img_name = first_name + '_' + last_name + '_' + fields[0] + '_' + fields[1] + '_' + fields[2] + '.jpg'
	server=subprocess.Popen(["wget", '--quiet', '-O', img_name, elem[0].attr('src') ], cwd='data')
	#print '%s %s %s %s' % (fields[1].split(' ')[1], fields[0], date.text(), img.attr('src'))
	imgs.append(img_name)

output_file = open(sys.argv[3],'w')
#We have the name and image, now lets get the conviction status
for f,l,d,s,r,i, in itertools.izip(first_names,last_names,dates,genders,races,imgs):
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
	output_file.write("%s,%s,%s,%s,%s,%d\n" % (f,l,s,r,i,status))

output_file.close()
