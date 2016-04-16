"""
Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt.
PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.
PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.
PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.
PubData is built on novel network programming and natural language processing algorithms that can
patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.
Future plans include adding web server support for PubData, and contributions from the open source community are welcome.
PubData is designed as a graphical user interface (GUI) software program written in the Python programming language
and PySide (Python binding of the cross-platform GUI toolkit Qt).
PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees
of any major bioinformatics database via a local computer network.
By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user
to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.
More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords
(e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and retrieve files
from the FTP servers of any major bioinformatics database directly from one centralized location.
By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.
PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD)
through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program.
This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO),
National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.
Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source
that makes use of any methods inspired by PubData.
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.
"""

# -*- coding: utf-8 -*-


import ftplib
import json
import os
import re
import socket
from Queue import Queue
from itertools import chain
from threading import Thread
from extras import general_style
from PyQt4.QtCore import pyqtSlot
from PySide import QtCore, QtGui, QtNetwork
from nltk.corpus import wordnet
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from searchpath import Path_results
from editserver import Edit_servers
from selectservers import SelectServers
from extras import SERVER_NAMES


class ftpWalker(object):
    """
    ==============
    ``ftpWalker``
    ----------
    .. py:class:: ftpWalker()
       :param :
       :type :
       :rtype: UNKNOWN
    .. note::
    .. todo::
    """
    def __init__(self, servername):
        """
        .. py:attribute:: __init__()
           :param servername:
           :type servername:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.servername = servername
        self.all_path = Queue()
        self.base, self.leading = self.find_leading()

    def find_leading(self):
        """
        .. py:attribute:: find_leading()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        base = []
        conn = ftplib.ftp(self.servername)
        conn.login()
        for p, dirs, files in self.Walk(conn, '/'):
            length = len(dirs)
            base.append((p, files))
            if length > 1:
                p = '/'.join(p.split('/')[1:])
                return base, [p + '/' + i for i in dirs]

    def listdir(self, connection, _path):
        """
        .. py:attribute:: listdir()
           :param connection:
           :type connection:
           :param _path:
           :type _path:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
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
        """
        .. py:attribute:: Walk()
           :param connection:
           :type connection:
           :param top:
           :type top:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        dirs, nondirs = self.listdir(connection, top)
        yield top, dirs, nondirs
        for name in dirs:
            new_path = os.path.join(top, name)
            for x in self.Walk(connection, new_path):
                yield x

    def Traverse(self, _path='/', word=''):
        """
        .. py:attribute:: Traverse()
           :param _path:
           :type _path:
           :param word:
           :type word:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        connection = ftplib.ftp(self.servername)
        try:
            connection.login()
        except:
            print 'Connection failed for path : ', _path
        else:
            try:
                connection.cwd(_path)
            except:
                pass
            else:
                for _path, _, files in self.Walk(connection, _path):
                    if word:
                        if any(word in file_name for file_name in files):
                            self.all_path.put((_path, files))
                    else:
                        self.all_path.put((_path, files))

    def run(self, word, threads=[]):
        """
        .. py:attribute:: run()
           :param word:
           :type word:
           :param threads:
           :type threads:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        print 'start threads...'
        os.mkdir(self.servername)
        for conn in self.leading:
            thread = Thread(target=self.Traverse, args=(conn, word))
            thread.start()
            threads.append(thread)
        for thread in threads:
                thread.join()


class ftpWindow(QtGui.QDialog):
    """
    ==============
    ``ftpWindow``
    ----------
    .. py:class:: ftpWindow()
       :param :
       :type :
       :rtype: UNKNOWN
    .. note::
    .. todo::
    """
    def __init__(self, parent=None):
        """
        .. py:attribute:: __init__()
           :param SelectServers:
           :type SelectServers:
           :param parent:
           :type parent:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        super(ftpWindow, self).__init__(parent)
        self.dbname = "PubData"
        self.mongo_cursor = self.mongo_connector()
        self.collection_names = self.mongo_cursor.collection_names()
        self.Select_s = SelectServers(SERVER_NAMES)
        self.Select_s.ok_button.clicked.connect(self.put_get_servers)
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("ftp name : ")
        self.ftpServerLabel = QtGui.QLabel('...')
        self.ftpServerLabel.setFrameStyle(frame_style)

        self.statusLabel = QtGui.QLabel("Please select name of a server")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.setDefault(True)

        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon('../images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)

        self.serverButton = QtGui.QPushButton('server list')
        self.downloadButton = QtGui.QPushButton("Download")
        self.downloadButton.setEnabled(False)

        self.addserverButton = QtGui.QPushButton("Add server to search")

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart search")
        self.dialog_box = QtGui.QInputDialog()

        self.EditserverButton = QtGui.QPushButton("Edit servers")
        self.UpdateserverButton = QtGui.QPushButton("Update custom servers")

        button_box = QtGui.QDialogButtonBox()
        button_box.addButton(self.downloadButton,
                             QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        button_box.addButton(self.EditserverButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.UpdateserverButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.downloadButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        button_box.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.addserverButton, QtGui.QDialogButtonBox.ActionRole)

        self.progressDialog = QtGui.QProgressDialog(self)
        self.fileList.itemActivated.connect(self.processItem)
        self.fileList.currentItemChanged.connect(self.enableDownloadButton)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.connectButton.clicked.connect(self.connectOrDisconnect)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.quitButton.clicked.connect(self.close)
        self.searchButton.clicked.connect(self.search)
        self.serverButton.clicked.connect(self.select)
        self.EditserverButton.clicked.connect(self.editservers)
        self.UpdateserverButton.clicked.connect(self.updateservers)
        self.addserverButton.clicked.connect(self.add_server_for_search)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self.senameLabel)
        top_layout.addWidget(self.ftpServerLabel)
        top_layout.addWidget(self.serverButton)
        top_layout.addWidget(self.cdToParentButton)
        top_layout.addWidget(self.connectButton)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.fileList)
        main_layout.addWidget(self.statusLabel)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("PubData")
        self.setStyleSheet(general_style)

    def getServerNames(self):
        """
        .. py:attribute:: getServerNames()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        try:
            with open('data/SERVER_NAMES.json')as f:
                return json.load(f)
        except IOError:
            with open('SERVER_NAMES.json', 'w') as f:
                json.dump(SERVER_NAMES, f, indent=4)
                message = """<p>Couldn't find the server file.</p>
                <p>Server names has beed rewrite, you can try again.</p>"""
                QtGui.QMessageBox.information(self,
                                              "QMessageBox.information()",
                                              message)

    def select(self):
        """
        .. py:attribute:: select()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        item, ok = QtGui.QInputDialog.getItem(self,
                                              "Select a server name ",
                                              "Server names:",
                                              SERVER_NAMES.keys(),
                                              0,
                                              False)
        if ok and item:
            self.ftpServerLabel.setText(SERVER_NAMES[item])
            self.servername = item

    @pyqtSlot(QtGui.QTreeWidget)
    def put_get_servers(self):
        """
        .. py:attribute:: put_get_servers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.selected_SERVER_NAMES = self.Select_s.selected_SERVER_NAMES
        # self.ftpServerLabel.text() = self.selected_SERVER_NAMES.pop(0)
        self.statusLabel.setText("Search in servers: {}".format(','.join(self.selected_SERVER_NAMES)))

    def updateservers(self):
        """
        .. py:attribute:: updateservers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.statusLabel.setText("Start updating ...")
        item, ok = QtGui.QInputDialog.getItem(self,
                                              "Select a server name ",
                                              "Season:",
                                              SERVER_NAMES.keys(),
                                              0,
                                              False)
        if ok and item:
            self.updateServerFile(item)

    def queue_traverser(self, queue):
        """
        .. py:attribute:: queue_traverser()
           :param queue:
           :type queue:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        while queue.qsize() > 0:
            yield queue.get()

    def updateServerFile(self, name):
        """
        .. py:attribute:: updateServerFile()
           :param name:
           :type name:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        try:
            self.statusLabel.setText("Start updating of {} ...".format(name))
            ftp_walker_ins = ftpWalker(SERVER_NAMES[name])
            ftp_walker_ins.run()
        except ftplib.error_temp as e:
            self.statusLabel.setText("Update failed")
            QtGui.QMessageBox.error(self,
                                    "QMessageBox.information()",
                                    e)
        except ftplib.error_perm as e:
            self.statusLabel.setText("Update failed")
            QtGui.QMessageBox.error(self,
                                    "QMessageBox.information()",
                                    e)
        except socket.gaierror as e:
            self.statusLabel.setText("Update failed")
            QtGui.QMessageBox.error(self,
                                    "QMessageBox.information()",
                                    e)
        else:
            for _path, files in queue_traverser(ftp_walker_ins.all_path):
                self.mongo_cursor[self.servername].insert(
                    {
                        'path': _path,
                        'files': files
                    }
                )

    def editservers(self):
        """
        .. py:attribute:: editservers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.wid = Edit_servers(SERVER_NAMES)
        self.wid.resize(350, 650)
        self.wid.setWindowTitle('Edit servers')
        self.wid.show()

    def sizeHint(self):
        """
        .. py:attribute:: sizeHint()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        return QtCore.QSize(800, 400)


    def connectOrDisconnect(self):
        """
        .. py:attribute:: connectOrDisconnect()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        if self.ftp:
            self.ftp.abort()
            self.ftp.deleteLater()
            self.ftp = None

            self.fileList.setEnabled(False)
            self.cdToParentButton.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.connectButton.setEnabled(True)
            self.connectButton.setText("Connect")
            self.setCursor(QtCore.Qt.ArrowCursor)

            return

        self.setCursor(QtCore.Qt.WaitCursor)

        self.ftp = QtNetwork.QFtp(self)
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()

        url = QtCore.QUrl(self.ftpServerLabel.text())
        if not url.isValid() or url.scheme().lower() != 'ftp':
            self.ftp.connectToHost(self.ftpServerLabel.text(), 21)
            self.ftp.login()
        else:
            self.ftp.connectToHost(url.host(), url.port(21))

            user_name = url.userName()
            if user_name:
                try:
                    # Python v3.
                    user_name = bytes(user_name, encoding='utf-8')
                except:
                    # Python v2.
                    pass

                self.ftp.login(QtCore.QUrl.fromPercentEncoding(user_name), url.password())
            else:
                self.ftp.login()

            if url.path():
                self.ftp.cd(url.path())

        self.fileList.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.connectButton.setText("Disconnect")
        self.statusLabel.setText("Connecting to ftp server %s..." % self.ftpServerLabel.text())

    def downloadFile(self):
        """
        .. py:attribute:: downloadFile()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        file_name = self.fileList.currentItem().text(0)

        if QtCore.QFile.exists(file_name):
            QtGui.QMessageBox.information(
                self,
                "ftp",
                "There already exists a file called %s in the current "
                "directory." % file_name)
            return

        self.outFile = QtCore.QFile(file_name)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(
                self,
                "ftp",
                "Unable to save the file %s: %s." % (file_name, self.outFile.errorString()))
            self.outFile = None
            return

        print self.fileList.currentItem().text(0)
        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText("Downloading %s..." % file_name)
        self.downloadButton.setEnabled(False)
        self.progressDialog.exec_()

    def cancelDownload(self):
        """
        .. py:attribute:: cancelDownload()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.ftp.abort()

    def ftpCommandFinished(self, _, error):
        """
        .. py:attribute:: ftpCommandFinished()
           :param _:
           :type _:
           :param error:
           :type error:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.setCursor(QtCore.Qt.ArrowCursor)
        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(
                    self,
                    "ftp",
                    """Unable to connect to the ftp server at %s. Please
                    check that the host name is correct.""" % self.ftpServerLabel.text())
                self.connectOrDisconnect()
                return

            self.statusLabel.setText("Logged onto %s." % self.ftpServerLabel.text())
            self.fileList.setFocus()
            self.downloadButton.setDefault(True)
            self.connectButton.setEnabled(True)
            return

        if self.ftp.currentCommand() == QtNetwork.QFtp.Login:
            self.ftp.list()

        if self.ftp.currentCommand() == QtNetwork.QFtp.Get:
            if error:
                self.statusLabel.setText("Canceled download of %s." % self.outFile.file_name())
                self.outFile.close()
                self.outFile.remove()
            else:
                self.statusLabel.setText("Downloaded %s to current directory." % self.outFile.file_name())
                self.outFile.close()

            self.outFile = None
            self.enableDownloadButton()
            self.progressDialog.hide()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            if not self.isDirectory:
                self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem(["<empty>"]))
                self.fileList.setEnabled(False)

    def addToList(self, urlInfo):
        """
        .. py:attribute:: addToList()
           :param urlInfo:
           :type urlInfo:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        item = QtGui.QTreeWidgetItem()
        item.setText(0, urlInfo.name())
        item.setText(1, str(urlInfo.size()))
        item.setText(2, urlInfo.owner())
        item.setText(3, urlInfo.group())
        item.setText(4, urlInfo.lastModified().toString('MMM dd yyyy'))

        if urlInfo.isDir():
            icon = QtGui.QIcon('../images/dir.png')
        else:
            icon = QtGui.QIcon('../images/file.png')
        item.setIcon(0, icon)

        self.isDirectory[urlInfo.name()] = urlInfo.isDir()
        self.fileList.addTopLevelItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.topLevelItem(0))
            self.fileList.setEnabled(True)

    def processItem(self, item):
        """
        .. py:attribute:: processItem()
           :param item:
           :type item:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        name = item.text(0)
        if self.isDirectory.get(name):
            self.fileList.clear()
            self.isDirectory.clear()
            self.currentPath += '/' + name
            self.ftp.cd(name)
            self.ftp.list()
            self.cdToParentButton.setEnabled(True)
            self.setCursor(QtCore.Qt.WaitCursor)

    def cdToParent(self):
        """
        .. py:attribute:: cdToParent()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()

        dirs = self.currentPath.split('/')
        if len(dirs) == 2:
            self.currentPath = '/'
            self.ftp.cd(self.currentPath)
            self.cdToParentButton.setEnabled(False)
        else:
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp.cd(self.currentPath)

        self.ftp.list()

    def change_path(self, path):
        """
        .. py:attribute:: change_path()
           :param path:
           :type path:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.ftp = QtNetwork.QFtp(self)
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.ftp.cd(path)
        self.ftp.list()

    def updateDataTransferProgress(self, readBytes, totalBytes):
        """
        .. py:attribute:: updateDataTransferProgress()
           :param readBytes:
           :type readBytes:
           :param totalBytes:
           :type totalBytes:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)

    def enableDownloadButton(self):
        """
        .. py:attribute:: enableDownloadButton()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        current = self.fileList.currentItem()
        if current:
            current_file = current.text(0)
            self.downloadButton.setEnabled(not self.isDirectory.get(current_file))
        else:
            self.downloadButton.setEnabled(False)

    def mongo_connector(self):
        """
        .. py:attribute:: mongo_connector()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        # Connect to mongoDB and return a connection object.
        try:
            c = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, error:
            sys.stderr.write("Could not connect to MongoDB: {}".format(error))
        else:
            print "Connected successfully"

        return c[self.dbname]

    def search(self):
        """
        .. py:attribute:: search()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        message = QtCore.QT_TR_NOOP(
            "<p>You have an error in your connection.</p>"
            "<p>Please select one of the server names and connect to it.</p>")
        text, ok = self.dialog_box.getText(self, "Search for file", 'Enter your keyword',QtGui.QLineEdit.Normal)
        if ok:
            try:
                total_find = {}
                regex = self.cal_regex(text)
                for servername in self.selected_SERVER_NAMES:
                    results = self.mongo_cursor[servername].find(
                        {"$or": [{"path": {"$regex": regex}}, {"files": {'$regex': regex}}]})
                    paths = [i['path'] for i in results]
                    total_find[servername] = paths
                match_path_number = sum(map(len, total_find.values()))
                if match_path_number:
                    self.wid = Path_results(SERVER_NAMES, total_find, match_path_number)
                    self.wid.resize(350, 650)
                    self.wid.setWindowTitle('Search')
                    self.wid.show()
                else:
                    message = """<p>No results.<p>Please try with another pattern.</p>"""
                    QtGui.QMessageBox.information(self, "QMessageBox.information()", message)

            except IOError:
                message = """<p>Unfortunately there is no collections with the name of this server in database.
                </p>Press OK to regural search.<p>It may takes between 2 to 10 minute.</p>"""
                QtGui.QMessageBox.information(self,
                                              "QMessageBox.information()",
                                              message)
                # self.fileList.clear()
                # self.isDirectory.clear()
                # self.setCursor(QtCore.Qt.WaitCursor)
                # self.regural_search(text,self.servername,self.ftpServerLabel.text())

    def cal_regex(self, text):
        """
        .. py:attribute:: cal_regex()
           :param text:
           :type text:
            :rtype: UNKNOWN
        .. note::
        """
        synonyms = wordnet.synsets(text)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        print lemmas
        pre_regex = '|'.join(lemmas)
        return re.compile(r'.*{}.*'.format(pre_regex), re.I)

    def regural_search(self, word, ftp, severname, sever_url):
        """
        .. py:attribute:: regural_search()
           :param word:
           :type word:
           :param ftp:
           :type ftp:
           :param severname:
           :type severname:
           :param sever_url:
           :type sever_url:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        try:
            ftp_walker_ins = ftp_walker(j)
            ftp_walker_ins.run(word)
        except ftplib.error_temp as e:
            QtGui.QMessageBox.information(self, "QMessageBox.information()", e)
        except ftplib.error_perm as e:
            QtGui.QMessageBox.information(self, "QMessageBox.information()", e)
        except socket.gaierror as e:
            QtGui.QMessageBox.information(self, "QMessageBox.information()", e)
        else:
            paths = ftp_walker_ins.all_path
            if paths:
                self.wid = Path_results(ftp, paths, servername)
                self.wid.resize(350, 650)
                self.wid.setWindowTitle('Regular search')
                self.wid.show()
            else:
                message = """<p>No results.<p>Please try with another pattern.</p>"""
                QtGui.QMessageBox.information(self, "QMessageBox.information()", message)

    def add_server_for_search(self):
        """
        .. py:attribute:: add_server_for_search()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.Select_s.resize(350, 650)
        self.Select_s.setWindowTitle('Select server for search')
        self.Select_s.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ftpWin_ = ftpWindow()
    COLLECTION_NAMES = ftpWin_.collection_names
    ftpWin = ftpWindow()
    COLLECTION_NAMES = ftpWin.collection_names
    ftpWin.show()
    sys.exit(ftpWin.exec_())
