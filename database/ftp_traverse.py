from ftpwalker import ftp_walker
import ftplib
from Queue import Queue
from datetime import datetime
from threading import Thread
import json
import socket


class Run(object):
    def __init__(self, name, server_name, root):
        self.all_path = Queue()
        self.server_name = server_name
        self.root = root
        self.name = name

    def find_leading(self):
        print "Find leading..."
        length = 2
        conn = ftplib.FTP(self.server_name)
        conn.login()
        fw = ftp_walker(conn, self.root)
        for p, dirs, files in fw.Walk(self.root):
            length = len(dirs)
            base = (p, files)
            if length > 1:
                p = '/'.join(p.split('/')[1:])
                length = length
                return base, [p + '/' + i for i in dirs]
        conn.quit()

    def traverse(self, root='/'):
        try:
            connection = ftplib.FTP(self.server_name)
            connection.login()
            connection.cwd(self.root)
        except Exception as exp:
            print exp.__str__()
        else:
            print "root is ", root
            fw = ftp_walker(connection, self.root.split('/')[-1])
            for _path, _, files in fw.Walk(root):
                self.all_path.put((_path, files))
                print _path
            connection.quit()

    def main_run(self):
        print '---' * 5, datetime.now(), '{}'.format(self.root), '---' * 5
        threads = []
        try:
            base, leading = self.find_leading()
            # parts = [leading[i:i + 5] for i in range(0, len(leading), 5)]
            # for part in parts:
            for conn in leading:
                thread = Thread(target=self.traverse, args=(conn.strip('/'),))
                thread.start()
                threads.append(thread)
            for thread in threads:
                    thread.join()

        except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
            print exp
        else:
            print '***' * 5, datetime.now(), '***' * 5
            l = []
            print 'creating list...'
            while self.all_path.qsize() > 0:
                l.append(self.all_path.get())
            print 'creating dict...'
            d = dict(base + l)
            print 'writing to json...'
            with open('{}.json'.format(self.name), 'w') as fp:
                json.dump(d, fp, indent=4, encoding='latin1')