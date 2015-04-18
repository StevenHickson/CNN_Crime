import sys
import subprocess

for i in range(int(sys.argv[1]),int(sys.argv[2])):
	fout = 'arrests.' + str(i)
	server=subprocess.Popen(["python", "get_arrests.py", str(i), fout], cwd='./')
	server.wait()
