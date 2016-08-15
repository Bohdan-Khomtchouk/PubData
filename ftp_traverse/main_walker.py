#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

from multiprocessing import Pool
from .traverse import Run
from datetime import datetime
import json
from collections import OrderedDict
from os import path as ospath
import sqlite3 as lite


class main_walker:
    def __init__(self, *args, **kwargs):
        self.servers = kwargs['servers']

    def walker(self):
        for root, name in self.servers.items():
            run = Run(name, "ftp.ncbi.nlm.nih.gov", root)
            base, leadings = run.find_leading(root, thread_flag=False)
            path, _ = base[0]
            leadings = [ospath.join(path, i.strip('/')) for i in leadings]
            print ("Root's leadings are: ", leadings)

            try:
                pool = Pool()
                pool.map(run.main_run, leadings)
            except Exception as exp:
                print(exp)
            else:
                print ('***' * 5, datetime.now(), '***' * 5)
                l = []
                print ('creating list...')
                while run.all_path.qsize() > 0:
                    l.append(run.all_path.get())
                print ('creating dict...')
                d = OrderedDict(base + l)
                print ('writing to json...')
                # self.create_json(d, name)
                self.update_table(d, name)

    def create_json(self, dictionary, name):
        json_path = ospath.join(*ospath.dirname(__file__).split('/')[:-1].__add__(
            ['database/json_files/{}.json'.format(name)]))
        with open('/' + json_path, 'w') as fp:
            json.dump(dictionary, fp, indent=4)

    def update_table(self, dictionary, name):
        conn = lite.connect('PubData.db')
        cursor = conn.cursor()
        name = name.lower().replace(' ', '_')
        for path, files in dictionary.items():
            for _file in files:
                cursor.execute(u"""INSERT OR IGNORE INTO {} (file_path, file_name) VALUES(?, ?);""".format(name), (path, _file))
                cursor.execute(u"""UPDATE '{}' SET file_name=? WHERE file_path=?;""".format(name), (_file, path))
        conn.commit()
