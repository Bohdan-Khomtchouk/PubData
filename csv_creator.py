#!/usr/bin/env python
# Copyright (C) 2015 Bohdan Khomtchouk, Thor Wahlestedt, Kelly Khomtchouk, Kasra Ahmadvand, and Claes Wahlestedt

# BioNetHub is a software program written in the Python programming language that can remotely access and
# navigate through the directory tree of any major bioinformatics database via a local computer network.
# By assembling all major bioinformatics databases under the roof of one software program, BioNetHub allows the user to avoid
# the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using
# an Internet browser. As such, BioNetHub allows researchers to access, view, and download files from the FTP
# servers of any major bioinformatics database directly from one centralized location. By using only a command-line environment
# (e.g., Terminal), BioNetHub allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the
# comfort of their local computer. BioNetHub is designed with network programming algorithms that can patch into any
# user-specified bioinformatics online database to be able to navigate, view, and download files directly from the command-line
# from one centralized location on a local computer network.


# BioNetHub is an ongoing bioinformatics software project fully financially supported by the
# United States Department of Defense (DoD) through the National Defense Science and Engineering
# Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under
# and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering
# Graduate (NDSEG) Fellowship, 32 CFR 168a.

# Please cite: "Khomtchouk et al.: 'BioNetHub: Python network programming engine for surfing the FTP servers of bioinformatics
# databases', 2015 (in preparation)" within any source that makes use of any methods
# inspired by BioNetHub.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------

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
