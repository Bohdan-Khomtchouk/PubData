#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Kelly Khomtchouk, Vytas Dargis-Robinson, and Claes Wahlestedt

# PubData is a genomics search engine for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into any user-specified bioinformatics online database and query its contents.
# Future plans include adding web server support for PubData, and contributions from the open source community are welcome.
# PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PySide (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and download files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  
# By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and download files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.
# PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.
# Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------

from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
import os
import json


class DBcreator:

    def __init__(self,dbname):
        self.dbname = dbname
        self.mongo_cursor = self.mongo_connector()

    def mongo_connector(self):
        # Connect to mongoDB and return a connection object.
        try:
            c = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, error:
            sys.stderr.write("Could not connect to MongoDB: {}".format(error))
        else:
            print "Connected successfully"

        return c[self.dbname]

    def importer(self):
        for _,_,files in os.walk('json_files/'):
            for file_name in files:
                print("Start inserting of {} ...".format(file_name))
                with open('json_files/{}'.format(file_name)) as f:
                    result = json.load(f,encoding='latin1')
                    for _path,file_names in result.iteritems():
                        collection_name = file_name.split('.')[0]
                        self.indexer(collection_name)
                        self.mongo_cursor[collection_name].insert(
                            {
                                'path': _path,
                                'files': file_names
                            }
                        )
                print ("Inserting finished.")

    def indexer(self,collection_name):
            self.mongo_cursor[collection_name].ensure_index(
                [
                    ('path', ASCENDING),
                ],
            )

if __name__ == '__main__':
    DBC = DBcreator('BioNetHub')
    DBC.importer()
