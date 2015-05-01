from collections import defaultdict
import sys
import random
import os.path
import itertools
from grab import Grab

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def verifyDate(s):
	if not isInt(s) and len(s.split('/')) == 3:
		return True
	else:
		return False

#image_1,image_3,image_2,name,url,gender,age,sex,dob,race,birth_date


imgs=[]
genders=[]
dobs=[]
races=[]
names=[]
name=""
dob=""
with open(sys.argv[1]) as f:
	for line in f:
		#parse line here
		fields = line.split(',')
		img1 = fields[0].split('/')[-1]
		img3 = fields[1].split('/')[-1]
		img2 = fields[2].split('/')[-1]
		if not isInt(fields[3]):
			name = fields[3]
		#url = fields[0]
		if fields[5] != "" and not isInt(fields[5]):
			gender = fields[5]
		#age = fields[6]
		if fields[7] != "" and not isInt(fields[7]):
			gender = fields[7]
		if fields[8] != "" and verifyDate(fields[8]):
			dob = fields[8]
		tmp = fields[10].rstrip('\r\n')
		if tmp != "" and verifyDate(tmp):
			dob = fields[10].rstrip('\r\n')
		if not isInt(fields[9]):
			race = fields[9]
		
		if name != "" and dob != "":
			#lets parse the dob for that weird error here:
			fields = dob.split('/')
			month = fields[0]	
			day = fields[1]	
			year = fields[2]
			if len(year) > 4 or int(month) > 12 or int(day) > 31:
				#invalid date, we need to fix this
				fixYear = month + day
				fixMonth = year[2:4]
				fixDay = year[4:6]
				dob = fixMonth + '/' + fixDay + '/' + fixYear

			if img1 != "" and os.path.isfile('dataset/' + img1):
				genders.append(gender)
				imgs.append(img1)
				names.append(name)
				dobs.append(dob)
				races.append(race)
			elif img2 != "" and os.path.isfile('dataset/' + img2):
				genders.append(gender)
				imgs.append(img2)
				names.append(name)
				dobs.append(dob)
				races.append(race)
			elif img3 != "" and os.path.isfile('dataset/' + img3):
				genders.append(gender)
				imgs.append(img3)
				names.append(name)
				dobs.append(dob)
				races.append(race)
print len(names)
print "GENDERS: "
print set(genders)
print "RACES: "
print set(races)

g = Grab()
output_file = open(sys.argv[2],'w')

for img, name, dob, race, gender in itertools.izip(imgs,names,dobs,races,genders):
	fields = name.split(' ')
	first = fields[0]
	numNames = len(fields)
	if len(fields[-1]) <= 3 and numNames > 2 and len(fields[numNames - 2]) > 3:
		last = fields[numNames -2]
	else:
		last = fields[-1]
	lookup = 'http://webapps6.doc.state.nc.us/opi/offendersearch.do?method=list&searchLastName=' + last + '&searchFirstName=' + first + '&searchDOB=' + dob + '&searchDOBRange=0'
	#print lookup
	g.go(lookup)
	if g.doc.text_search(u'Nothing found'):
		status=0
	else:
		elem = g.doc.select('//tr/td[@class="tablelink"]/a')
		#print '%s' % elem[0].attr('href')
		if len(elem) > 1:
			repeater = 1
		else:
			repeater = 0
		g.go('http://webapps6.doc.state.nc.us/opi/' + elem[0].attr('href'))
		if g.doc.text_search(u'INMATE'):
			status=2
		elif g.doc.text_search(u'PROBATION'):
			status=1
		else:
			status=0
	full = '/home/steve/inmates/dataset/' + img
	output_file.write("%s,%s,%s,%s,%s,%s,%d,%d\n" % (first,last,dob,gender,race,full,repeater,status))

output_file.close()
