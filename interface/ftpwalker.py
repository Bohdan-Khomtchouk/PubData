#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import ftplib
from os import path
from threading import Thread
from Queue import Queue
from datetime import datetime
import json
import socket


class ftp_walker(object):
    def __init__(self, root, server_addr):
        self.length = 2
        self.server_addr = server_addr
        self.all_path = Queue()
        self.base, self.leading = self.find_leading(root)

    def find_leading(self, root):
        base = []
        conn = ftplib.FTP(self.server_addr)
        conn.login()
        for p, dirs, files in self.Walk(conn, root):
            length = len(dirs)
            base.append((p, files))
            if length > 1:
                p = '/'.join(p.split('/')[1:])
                self.length = length
                return base, [p + '/' + i for i in dirs]
        conn.quit()

    def listdir(self, connection, _path):
        file_list, dirs, nondirs = [], [], []
        try:
            connection.cwd(_path)
        except:
            return [], []

        connection.retrlines('LIST', lambda x: file_list.append(x.split()))
        for info in file_list:
            ls_type, name = info[0], info[-1]
            if ls_type.startswith('d'):
                dirs.append(name)
            else:
                nondirs.append(name)
        return dirs, nondirs

    def Walk(self, connection, top):
        dirs, nondirs = self.listdir(connection, top)
        yield top, dirs, nondirs
        for name in dirs:
            new_path = path.join(top, name)
            for x in self.Walk(connection, new_path):
                yield x

    def Traverse(self, _path='/'):
        try:
            connection = ftplib.FTP(self.server_addr)
            connection.login()
        except Exception as exp:
            print 'Connection failed for path : ', _path, exp.__str__()
        else:
            for _path, _, files in self.Walk(connection, _path):
                self.all_path.put((_path, files))
                print _path
            connection.quit()

    def run(self, threads=[]):
        print 'start threads...'
        parts = [self.leading[i:i + 4] for i in range(0, len(self.leading), 4)]
        for part in parts:
            for conn in part:
                thread = Thread(target=self.Traverse, args=(conn,))
                thread.start()
                threads.append(thread)
            for thread in threads:
                    thread.join()



"""server_names = {'Ensembl Genome Browser': 'ftp.ensembl.org',
                'The Arabidopsis Information Resource': 'ftp.arabidopsis.org/home',
                'National Center for Biotechnology Information': 'ftp.ncbi.nlm.nih.gov',
                'O-GLYCBASE': 'ftp.cbs.dtu.dk',
                'PairsDB': 'nic.funet.fi'}"""


def main_run(address, name, root):
    print '---' * 5, datetime.now(), '{}'.format(address), '---' * 5
    try:
        FT = ftp_walker(root, address)
        FT.run()
    except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
        print exp
    else:
        print '***' * 5, datetime.now(), '***' * 5
        l = []
        print 'creating list...'
        while FT.all_path.qsize() > 0:
            l.append(FT.all_path.get())
        print 'creating dict...'
        d = dict(FT.base + l)
        print 'writing to json...'
        with open('{}.json'.format(name), 'w') as fp:
            json.dump(d, fp, indent=4, encoding='latin1')
