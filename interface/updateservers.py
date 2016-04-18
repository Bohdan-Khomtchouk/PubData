import ftplib
from os import path
from datetime import datetime
import json
import socket
from extras import SERVER_NAMES
import sqlite3 as lite


class Update(object):
    def __init__(self, server_addr, last_update_time):
        self.length = 2
        self.server_addr = server_addr
        self.all_path = {}
        self.base, self.leading = self.find_leading()
        self.last_update = last_update_time

    def listdir(self, connection, _path):
        file_list, dirs, nondirs = [], [], []
        try:
            connection.cwd(_path)
        except:
            return [], []

        connection.retrlines('LIST', lambda x: file_list.append(x.split()))
        for info in file_list:
            ls_type, date_s, name = info[0], '-'.join(info[5:8]), info[-1]
            try:
                if ':' in date_s:
                    date_s = datetime.strftime(date_s, '%b-%d-%H:%M')
                else:
                    date_s = datetime.strftime(date_s, '%b-%d-%Y')
            except Exception as exp:
                print exp
            else:
                if date_s > self.last_update_time:
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
                self.all_path[_path] = files
            connection.quit()


class MainUpdate(Update):
    def __init__(self, manual_list=None):
        self.update_dict = None
        self.manual_list = manual_list

    def cal_new_dict(self):
        for i, j in SERVER_NAMES.items():
            print '---' * 5, datetime.now(), '{}'.format(j), '---' * 5
            try:
                self.Traverse()
            except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
                print exp
            else:
                print '***' * 5, datetime.now(), '***' * 5
                if self.all_path:
                    with open('../database/json_files/{}.json'.format(i)) as f:
                        old_dict = json.load(f)
                    for k, v in self.all_path:
                        old_dict[k] = v
                self.update_dict = old_dict

    def update_all(self):
        for name, addr in SERVER_NAMES.items():
            table_name = '_'.join(map(str.lower, name.split()))
            self.update_database(table_name)

    def update_manual(self):
        for name in self.manual_list:
            table_name = '_'.join(map(str.lower, name.split()))
            self.update_database(table_name)

    def update_database(self, table_name):
        conn = lite.connect('PubData.db')
        curs = conn.cursor()
        id_ = 0
        for path_add, file_names_ in self.update_dict.items():
            for name in file_names_:
                id_ += 1
                curs.execute("""INSERT INTO {} (id, file_path, file_name)
                                VALUES (?, ?, ?)""".format(table_name), (id_, path_add, name))
