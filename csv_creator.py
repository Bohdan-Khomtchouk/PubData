import os,csv
from tempfile import NamedTemporaryFile
import shutil


def create_directory_structure(rootdir,d={}):

	import csv
	with open('newcsv.csv', 'wb') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',')
	    for path, _, files in os.walk(rootdir):
	    	spamwriter.writerow([path]+files)


def change_path(file_name,source,destination,tempfile = NamedTemporaryFile(delete=False)):

	with open('newcsv.csv', newline='') as infile,tempfile:
    	spamreader = csv.reader(csvfile, delimiter=',')
    	spamwriter = csv.writer(tempfile, delimiter=',')
    	for row in spamreader:
    		if row[0]==source and file_name in row:
    			row.remove(file_name)
    			spamwriter.writerow(row)
    		else:
    			spamwriter.writerow(row)

    shutil.move(tempfile.name, file_name)

def remove_path(path,file_name=''):

	with open('newcsv.csv', newline='') as infile,tempfile:

	    	spamreader = csv.reader(csvfile, delimiter=',')
	    	spamwriter = csv.writer(tempfile, delimiter=',')
	    	for row in spamreader:
	    		if row[0]==path:
	    		  if file_name:
	    			row.remove(file_name)
	    			spamwriter.writerow(row)
	    		  else:
	    			continue
	    		spamwriter.writerow(row)


	shutil.move(tempfile.name, file_name)





#		(next(fname for fname in value if ) for key,value in dic_structure.iteritems()) #in python 3 ic_structure.views()
