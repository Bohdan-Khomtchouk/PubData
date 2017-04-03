"""
=====
runwalker.py
=====

This module is contain the `ftpwalker` class which is responsible for
running a new walker.

============================

"""

from . import main_walker
from os import path, makedirs, listdir
from PyQt4 import QtGui
import shutil
from . import checkplatform
import re


class ftpwalker:
    """
    ==============

    ``ftpwalker``
    ----------
    You can pass following arguments to class's caller at instantiation's time.
    server_name: The name of server
    url: The corresponding url
    root: The root path that you want to start the traversing from.
    daemon: Daemonization flag, which should be a boolean value (True, False)
    json_path: Corresponding path for saving the final json file.
    .. py:class:: ftpwalker()

    .. note::

    Example

    .. code-block:: python

    """
    def __init__(self, server_name, url, root='/', daemon=False):
        """
        .. py:attribute:: __init__()

           :param server_name: name of server
           :type server_name: str
           :param url: server's url
           :type url: str
           :param root: traversing start root
           :type root: str
           :param daemon: daemon flag
           :type daemon: boolean
           :rtype: None
        """
        self.name = re.sub(r'\W', '_', server_name)
        self.url = url
        platform_name = checkplatform.check()
        if daemon:
            print("Platform {}".format(platform_name))
            if platform_name in {"Linux", "Mac"}:
                from daemons.unixdaemon import Daemon as daemon_obj
                self.daemon_obj = daemon_obj()
                try:
                    self.daemon_obj.stop()
                except Exception as exc:
                    print("Exception on stopping the daemon:  {}".format(exc))
            else:
                from daemons import windaemon as daemon_obj
                self.daemon_obj = daemon_obj
                try:
                    self.daemon_obj.stop()
                except Exception as exc:
                    print("Exception:  {}".format(exc))
        self.daemon = daemon
        try:
            home = path.expanduser("~")
            server_path = path.join(home, "FTPwalkerfile/", self.name)
        except Exception as exc:
            raise Exception("Please enter a valid name. {}".format(exc))
        else:
            self.server_path = server_path
        self.m_walker = main_walker.main_walker(server_name=self.name,
                                                url=self.url,
                                                server_path=self.server_path,
                                                root=root)

    def check_state(self):
        """
        .. py:attribute:: check_state()
        Check the current state. If a wanlker kas been run already
        it asks for continue or aborting, otherwise it starts the traversing.

           :rtype: None
        """
        try:
            if path.isdir(self.server_path):
                if len(listdir(self.server_path)) > 0:
                    self.path_exit()
                else:
                    self.path_not_exit(False)
            else:
                self.path_not_exit(True)
        except:
            if self.daemon:
                self.daemon_obj.stop()
            raise

    def path_exit(self):
        """
        .. py:attribute:: path_exit()

        Runs if If a wanlker kas been run already.

           :rtype: None

        """
        while True:
            quit_msg = input("""It seems that you've already
started traversing a server with this name.
Do you want to continue with current one(Y/N)?: """)
            reply = QtGui.QMessageBox.question('Message',
                                               quit_msg,
                                               QtGui.QMessageBox.Yes,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                print("Start resuming the {} server...".format(self.name))
                if self.daemon:
                    self.daemon_obj.start(self.m_walker.Process_dispatcher, True)
                else:
                    self.m_walker.Process_dispatcher(True)
                break
            else:
                # deleting the directory
                shutil.rmtree(self.server_path)
                makedirs(self.server_path)
                if self.daemon:
                    self.daemon_obj.start(self.m_walker.Process_dispatcher, False)
                else:
                    self.m_walker.Process_dispatcher(False)
                break

    def path_not_exit(self, create_dir):
        """
        .. py:attribute:: path_not_exit()
        Runs if there is no unsuccessful traversed server with this name.

           :param create_dir: A boolean value for creating a directory for this server
           in order to preserving the temp files.
           :type create_dir: boolean
           :rtype: None

        """
        # create the directory
        if create_dir:
            makedirs(self.server_path)
        if self.daemon:
            self.daemon_obj.start(self.m_walker.Process_dispatcher, False)
        else:
            self.m_walker.Process_dispatcher(False)
