#!/usr/bin/env python
# Copyright (C) 2015 Bohdan Khomtchouk, Thor Wahlestedt, Kelly Khomtchouk, and Claes Wahlestedt

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

import ftplib
import os, sys

nonpassive = False
request = True
temp = 0
dirname = '.'
print '1. ftp.ensembl.org/'
print '2. hgdownload.cse.ucsc.edu/'
print '3. ftp.uniprot.org/'
print '4. ftp.flybase.net/'
print '5. ftp.xenbase.org/'
print '6. ftp.arabidopsis.org/home/'
print '7. rgd.mcw.edu/'
print '8. ftp.ncbi.nlm.nih.gov/'
website = ('Please enter the corresponding number for the database you\'d like to access. \n')

sitename = None
while True:
	database = raw_input(website)
	if (database == '1'):
		sitename = 'ftp.ensembl.org'
		break
	elif (database == '2'):
		sitename = 'hgdownload.cse.ucsc.edu'
		break
	elif (database == '3'):
		sitename = 'ftp.uniprot.org'
		break
	elif (database == '4'):
		sitename = 'ftp.flybase.net'
		break
	elif (database == '5'):
		sitename = 'ftp.xenbase.org'
		break
	elif (database == '6'):
		sitename = 'ftp.arabidopsis.org/home'
		break
	elif (database == '7'):
		sitename = 'rgd.mcw.edu'
		break
	elif (database == '8'):
		sitename = 'ftp.ncbi.nlm.nih.gov'
		break
	else:
		print 'That\'s not a correct input.'


#prompt = 'Username: '
#username = raw_input(prompt)
#prompt1 = 'Password: '
#password = raw_input(prompt1)
#userinfo = (username, password)

proof = []
proof2 = []
proof3 = []
print ('Connecting...')
connection = ftplib.FTP(sitename)
connection.login()
connection.cwd('/')
sitename+='/'
connection.cwd(dirname)
connection.dir(proof.append)
for u in proof:
	print u + '\n'
print 'NOTE: If the permissions line of a file/directory begins with a \'d\', it\'s a directory. Otherwise, it\'s a file. If the permissions line of a file/directory begins with a \'l\', it\'s a symbolic link; to download this entry, type only what is written to the left of the arrow (more on this below).\n'
while True:
	prompt2 = 'If you\'d like to go on and enter a directory name, type: name_of_my_directory.\n\nIf you\'d like to go back one directory, type: back.\n\nIf you\'d like to download a file, first type: download. Then type: name_of_my_file. For symbolic links, make sure to type: name_of_my_file_left_of_arrow.\n\nIf you\'d like to go back to the start of the directory tree, type: home.\n\nIf you\'d like to quit, type: quit.\n'
	choice2 = raw_input(prompt2)
	
	if (choice2=='home'):
		connection.cwd('/')
	elif (choice2=='quit'):
		break
	elif (choice2=='back'):
		if (temp==1):
			connection.cwd('/')
		elif (temp>1):
			x = len(sitename)
			y = 0
			z = 0
			while (y<2):
				if (sitename[x-1]=='/'):
					y+=1
				x-=1
			backURL = sitename[0 : x+1]
			finalURL = backURL[len(control): len(backURL)]
			connection.cwd(finalURL)
	elif (choice2=='download'):
		while (request):	
			prompt4 = 'Which file would you like to download? (please include file type)\n'
			choice4 = raw_input(prompt4)
			print ('Downloading...')
			file = open(choice4, 'wb')
			connection.retrbinary('RETR %s' % choice4, file.write)
			prompt5 = 'Would you like to download another?\n'
			choice5 = raw_input(prompt5)
			if (choice5=='No' or choice5=='N' or choice5=='no' or choice5=='n'):
				request = False
				check = False
		connection.quit()
		file.close()
	else:
		connection.cwd(choice2)
		sitename+=choice2
		sitename+='/'
	if (choice2!='download'):
		files = []
		connection.dir(files.append)
		for u in files:
			print u + '\n'
	temp+=1
	
if nonpassive:
	connection.set_pasv(False)