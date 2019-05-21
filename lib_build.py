# (c)2019 savagerebirth.com
"""A small script to compile py to pyc for placement in a zip"""

import py_compile
import os

for root, subdirs, filenames in os.walk('.'):
	for filename in filenames:
		if filename.endswith('.py'):
			print("compiling "+root+"/"+filename+" to zip/"+root+"/"+filename+'c')
			py_compile.compile(root+'/'+filename, 'zip/'+root+'/'+filename+'c')

