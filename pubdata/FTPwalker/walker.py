"""
=====
walker.py
=====

Traverse the FTP servers with BFS algorithm.

============================

"""

from os import path as ospath


class ftp_walker(object):
    """
    ==============

    ``ftp_walker``
    ----------

    .. py:class:: ftp_walker()

    This class is contain corresponding functions for traversing the FTP
    servers using BFS algorithm.

    """
    def __init__(self, connection, resume=False):
        """
        .. py:attribute:: __init__()


           :param connection: FTP connection object
           :type connection: ftplib.connection
           :rtype: None

        """
        self.connection = connection
        self.resume = resume

    def listdir(self, _path):
        """
        .. py:attribute:: listdir()

        return files and directory names within a path (directory)
           :param _path: path of a directory
           :type _path: str
           :rtype: tuple

        """
        file_list, dirs, nondirs = [], [], []
        try:
            self.connection.cwd(_path)
        except Exception as exp:
            print ("the current path is : ", self.connection.pwd(), exp.__str__(),_path)
            return [], []
        else:
            self.connection.retrlines('LIST', lambda x: file_list.append(x.split()))
            for info in file_list:
                ls_type, name = info[0], info[-1]
                if ls_type.startswith('d'):
                    dirs.append(name)
                else:
                    nondirs.append(name)
            return dirs, nondirs

    def walk_resume(self, _path, base_name, root=None):

        def inner_walk(parent, base_name):
            # print("Parent is {}".format(parent))
            dirs, _ = self.listdir(parent)
            # print("dirs are : {}".format(dirs))
            diffs = set(dirs) - {base_name}
            for name in diffs:
                name = ospath.join(parent, name)
                yield from self.walk(name)
        if _path == root:
            yield None
            yield from self.walk(_path)
        else:
            parent = ospath.dirname(_path)
            base_name = ospath.basename(_path)
            yield from self.walk(_path)
            yield from inner_walk(parent, base_name)
            while parent != root:
                base_name = ospath.basename(parent)
                parent = ospath.dirname(parent)
                yield from inner_walk(parent, base_name)

    def walk(self, path='/'):
        """
        .. py:attribute:: Walk()

        Walk through FTP server's directory tree
           :param path: Leading path
           :type path: str
           :rtype: generator (path and files)

        """
        dirs, nondirs = self.listdir(path)
        yield path, dirs, nondirs
        for name in dirs:
            path = ospath.join(path, name)
            yield from self.walk(path)
            self.connection.cwd('..')
            path = ospath.dirname(path)
