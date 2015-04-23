import sys
import subprocess
from grab import Grab
from glob import glob
import shlex

g = Grab()

path = "http://mugshots.com"
g.go(path + "/US-Counties/North-Carolina/")

for elem in g.doc.select('//div/ul[@class="categories"]/li/a'):
	print path + elem.attr('href')
	for i in range(1,85):
		fout = 'arrests.' + str(i)
		server=subprocess.Popen(["python", "get_arrests.py", path + elem.attr('href'), str(i), fout], cwd='./')
		server.wait()

	files = ' '.join(glob('arrests.*'))
	command = "cat " + files
	args = shlex.split(command)
	with open('tmp.txt', 'a+') as output:
		server=subprocess.Popen(args, cwd='./', stdout=output)
		server.wait()
	command = "rm " + files
	args = shlex.split(command)
	server=subprocess.Popen(args, cwd='./')
	server.wait()
