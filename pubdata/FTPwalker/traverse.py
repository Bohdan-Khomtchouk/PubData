"""
=====
traverse.py
=====

This module is responsible for dispatching the threads between subdirectories.

============================

"""

from . import walker
import ftplib
from multiprocessing import Manager
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
import socket
from os import path as ospath
import json
import csv


class Run(object):
    """
    ==============

    ``Run``
    ----------

    .. py:class:: Run()

    Main class for threads dispatcher.

    """
    def __init__(self, name, server_url, root, server_path, meta_path, resume):
        """
        .. py:attribute:: __init__()


           :param server_name: name of server
           :type server_name: str
           :param url: server's url
           :type url: str
           :param root: traversing start root
           :type root: str
           :param server_path: corresponding path for saving temporary files
           :type server_path: str
           :param resume: resume flag for resuming the traversing
           :type resume: bool
           :rtype: None

        """
        m = Manager()
        self.all_path = m.Queue()
        self.server_url = server_url
        self.root = root
        self.name = name
        self.server_path = server_path
        self.meta_path = meta_path
        self.resume = resume

    def find_leading(self, top):
        """
        .. py:attribute:: find_leading()


           :param top: The top root for starting the traversing
           :type top: str
           :param thread_flag: shows if leadings are for threads or not
           :type thread_flag: boolean
           :rtype: tuple

        """
        print ("Find leading...")
        conn = ftplib.FTP(self.server_url)
        conn.login()
        fw = walker.ftp_walker(conn)
        dirs, files = fw.listdir(top)
        return files, dirs
        conn.quit()

    def traverse_branch(self, args):
        """
        .. py:attribute:: traverse_branch()


           :param root: The root path for start traversing
           :type root: str
           :rtype: None

        """
        if self.resume:
            _path = args
        else:
            _path, root = args
        try:
            connection = ftplib.FTP(self.server_url)
            connection.login()
            # connection.cwd(root)
        except Exception as exp:
            print ("Couldn't create the connections for thread {}".format(exp))
        else:
            # file_names = listdir(self.server_path)
            fw = walker.ftp_walker(connection, self.resume)
            if self.resume:
                walker_obj = fw.walk_resume(_path, self.root)
                next(walker_obj)
            else:
                walker_obj = fw.walk(root)
            root_name = ospath.basename(_path)
            # csv_writer_lock = threading.Lock()
            with open('{}/{}.csv'.format(self.server_path, root_name), 'a+') as f:
                csv_writer = csv.writer(f)
                try:
                    for _path, dirs, files in walker_obj:
                        # self.all_path.put((_path, files))
                        # with csv_writer_lock:
                        csv_writer.writerow([_path] + files)
                        print("Path: {} <-------> dirs: {}".format(_path, dirs))
                except Exception as exc:
                    print(exc)
                else:
                    with open(self.meta_path, 'r+') as f:
                        try:
                            meta = json.load(f)
                            meta.setdefault('traversed_subs', []).append(root_name)
                        except:
                            pass
                        else:
                            f.seek(0)
                            json.dump(meta, f)

            connection.quit()

    def find_all_leadings(self, leadings):
        """
        .. py:attribute:: find_all_leadings()


           :param leadings: find all the leadings for all the subdirectories
           :type leadings: list
           :rtype: dict

        """
        return {path: self.find_leading(path) for path in leadings}

    def main_run(self, args):
        """
        .. py:attribute:: main_run()
        Run threads by passing a leading directory to `traverse_branch` function.

           :param args: a tuple contain root and another tuple contains base and
           leadings. The root is the path of parent directory (assigned to a process)
           base is a tuple contain the path of sub-directory and file names that are
           associated with.
           :type args: iterable
           :rtype: None

        """
        if self.resume:
            root, leadings = args
            base = ['/']
        else:
            root, (base, leadings) = args
        print ('---' * 5, datetime.now(), '{}'.format(root), '---' * 5)
        try:
            # base, leadings = self.find_leading(root)
            # print("base and leadings for {} --> {}, {}".format(root, base, leadings))
            if not self.resume:
                leadings = [(ospath.join('/', root, i.strip('/')), root) for i in leadings]
            if leadings:
                pool = ThreadPool()
                pool.map(self.traverse_branch, leadings)
                pool.close()
                pool.join()
            else:
                self.all_path.put(base[0])
        except (ftplib.error_temp, ftplib.error_perm, socket.gaierror) as exp:
            print(exp)
