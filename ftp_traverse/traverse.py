#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

from .ftpwalker import ftp_walker
import ftplib
from multiprocessing import Manager
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
import socket
from os import path as ospath


class Run(object):
    def __init__(self, name, server_url, root):
        m = Manager()
        self.all_path = m.Queue()
        self.server_url = server_url
        self.root = root
        self.name = name

    def find_leading(self, top, thread_flag=True):
        print ("Find leading...")
        length = 2
        conn = ftplib.FTP(self.server_url)
        conn.login()
        fw = ftp_walker(conn)
        for p, dirs, files in fw.Walk(top):
            length = len(dirs)
            base = [(p, files)]
            if length > 1:
                p = '/'.join(p.split('/')[1:])
                length = length
                return base, dirs
            elif thread_flag:
                return base, []
        conn.quit()

    def traverse_branch(self, root='/'):
        try:
            connection = ftplib.FTP(self.server_url)
            connection.login()
            # connection.cwd(root)
        except Exception as exp:
            print (exp.__str__())
        else:
            fw = ftp_walker(connection)
            for _path, _, files in fw.Walk(root):
                self.all_path.put((_path, files))
            connection.quit()

    def main_run(self, root):
        print ('---' * 5, datetime.now(), '{}'.format(root), '---' * 5)
        try:
            base, leadings = self.find_leading(root)
            leadings = [ospath.join('/', root, i.strip('/')) for i in leadings]
            if leadings:
                pool = ThreadPool()
                pool.map(self.traverse_branch, leadings)
                pool.close()
                pool.join()
            else:
                self.all_path.put(base[0])
        except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
            print (exp)
