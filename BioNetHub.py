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

import csv
import ftplib


class Search(object):

    def __init__(self,file_name):
    	self.name=file_name

	def search(self):
		with open('newcsv.csv', 'wb') as csvfile:
		    spamreader = csv.writer(csvfile, delimiter=',')
		    for row in spamreader:
		    	if self.name in row:
		        	return row[0]
	
	def download(self):
		
		try:
			print ('Connecting...')
			connection= ftplib.FTP('ftp.uniprot.org')
			connection.login()
			path=search()
			connection.cwd(path)
			print ("""Connection successful...
				\n-----------------------\n""")
			
			print ('Downloading...')

			file_path=raw_input("""Enter the path and name of file for saving :
				( for example : /home/username/Desktop/bio.xml )""")

			with open('bio', 'wb') as f:
				connection.retrbinary('RETR '+self.name, f.write)
			print ('Downloading complete')
		except:
			print ("Connection unsuccessful...")

	def server_selecter(self):

		server_names={'1':'ftp.ensembl.org/',
		 '2':'hgdownload.cse.ucsc.edu/',
		 '3':'ftp.uniprot.org/',
		 '4':'ftp.flybase.net/',
		 '5':'ftp.xenbase.org/',
		 '6':'ftp.arabidopsis.org/home/',
		 '7':'rgd.mcw.edu/',
		 '8':'ftp.ncbi.nlm.nih.gov/'}

		for i,s_name in server_names.iteritems():
		 	print "{}.{}".format(i,s_name)

		website = ('Please enter the corresponding number for the database you\'d like to access. \n')

		while True:
			database = raw_input(website)
			try:
				sitename=server_names[database]
				break
			except:
				print 'That\'s not a correct input.'
				
		return sitename