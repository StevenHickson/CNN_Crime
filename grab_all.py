import sys
import subprocess
from grab import Grab

g = Grab()

path = "http://mugshots.com"
g.go(path + "/US-Counties/North-Carolina/")

for elem in g.doc.select('//div/ul[@class="categories"]/li/a'):
	print path + elem.attr('href')
	for i in range(1,85):
		fout = 'arrests.' + str(i)
		server=subprocess.Popen(["python", "get_arrests.py", path + elem.attr('href'), str(i), fout], cwd='./')
		server.wait()

	server=subprocess.Popen(["cat", "arrests.*", ">>", "tmp.txt"], cwd='./')
	server.wait()
	server=subprocess.Popen(["rm", "arrests.*"], cwd='./')
	server.wait()
