from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
import os
import json


class DBcreator:

    def __init__(self,dbname):
        self.dbname = dbname
        self.collection_name = "directoryTree"
        self.mongo_cursor = self.mongo_connector()
        self.indexer()

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
                print("Start inserting of {} ...".format(file_name)
                with open('json_files/{}'.format(file_name)) as f:
                    result = json.load(f,encoding='latin1')
                    for _path,file_names in result.iteritems():
                        self.mongo_cursor[self.collection_name].insert(
                            {
                                'path': _path,
                                'files': files
                            }
                        )
                print ("Inserting finished.")

    def indexer(self):
            self.mongo_cursor[self.collection_name].ensure_index(
                [
                    ('path', ASCENDING),
                ],
            )

if __name__ == '__main__':
    DBC = DBcreator('BioNetHub')
    DBC.importer()
