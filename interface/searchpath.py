#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.
# Future plans include adding web server support for PubData, and contributions from the open source community are welcome.
# PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PySide (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  
# By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and retrieve files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.
# PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.
# Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------

from extras import general_style
from PyQt4.QtCore import pyqtSlot

from PySide import QtCore, QtGui, QtNetwork


class Path_results(QtGui.QDialog):    
    """
    ==============
    ``Path_results``
    ----------
    .. py:class:: Path_results()
       :param :
       :type :
       :rtype: UNKNOWN
    .. note::
    .. todo::
    """
    def __init__(self, server_names, total_find, path_number, parent=None):
        """
        .. py:attribute:: __init__()
           :param server_names:
           :type server_names:
           :param total_find:
           :type total_find:
           :param path_number:
           :type path_number:
           :param parent:
           :type parent:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        super(Path_results, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.path_number = path_number
        self.setLayout(self.main_layout)
        self.total_find = total_find
        self.SERVER_NAMES = server_names
        self.h_layout = QtGui.QHBoxLayout()
        self.countLabel = QtGui.QLabel("{} Results founded!".format(self.path_number))
        top_layout = QtGui.QVBoxLayout()
        top_layout.addWidget(self.countLabel)
        self.main_layout.addLayout(top_layout)
        self.main_layout.insertLayout(0, self.h_layout)
        self.list_a = QtGui.QTreeWidget()
        self.list_a.setHeaderLabels(['Matched paths', 'Server name'])
        self.dialog_box = QtGui.QInputDialog()
        for s_name, all_path in self.total_find.items():
            for p in all_path:
                item = QtGui.QTreeWidgetItem()
                item.setText(0, p)
                item.setText(1, s_name)
                self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)
        self.setStyleSheet(general_style)

        self.list_a.itemDoubleClicked.connect(self.doubleClicked_path)

    @pyqtSlot(QtGui.QTreeWidget)
    def doubleClicked_path(self, item):
        """
        .. py:attribute:: doubleClicked_path()
           :param item:
           :type item:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.wind = Sub_path(self.SERVER_NAMES[item.text(1)], item.text(0))
        self.wind.resize(450, 650)
        self.wind.setWindowTitle('Sub-path')
        self.wind.show()

class Sub_path(QtGui.QDialog):
    """
    ==============
    ``Sub_path``
    ----------
    This class will open a path from the result of user's search (see :ref:`Path_results`). 
    .. note::
    .. todo::
    """
    def __init__(self, root, path, parent=None):
        """
        .. py:attribute:: __init__()
           :param root: The server's root address (ftp URL)
           :type root: str
           :param path: The intended path
           :type path: str
        .. note::
        .. todo::
        """
        super(Sub_path, self).__init__(parent)
        self.root = root
        self.path = path
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("ftp name : ")
        self.senameLabel.setText(root)
        self.ftpServerLabel = QtGui.QLabel('...')
        self.ftpServerLabel.setFrameStyle(frame_style)

        # self.statusLabel = QtGui.QLabel("Please select the name of an ftp server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.downloadButton = QtGui.QPushButton("Download")
        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon('../images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.fileList.itemActivated.connect(self.processItem)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)

        button_box = QtGui.QDialogButtonBox()
        button_box.addButton(self.downloadButton, QtGui.QDialogButtonBox.ActionRole)
        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self.senameLabel)
        top_layout.addWidget(self.cdToParentButton)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.fileList)
        # main_layout.addWidget(self.statusLabel)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle("PubData")
        self.setStyleSheet(general_style)
        self.connectOrDisconnect()

    def connectOrDisconnect(self):
        """
        Connecting to and disconnecting from FTP host.
        .. py:attribute:: connectOrDisconnect()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        if not self.ftp:
            print 'create new FTP connection'
            self.ftp = QtNetwork.QFtp(self)

        self.setCursor(QtCore.Qt.WaitCursor)
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()
        print self.path
        url = QtCore.QUrl(self.root)
        if not url.isValid() or url.scheme().lower() != 'ftp':
            self.ftp.connectToHost(self.root, 21)
            self.ftp.login()
            self.setCursor(QtCore.Qt.WaitCursor)
            self.fileList.clear()
            self.currentPath = '/'.join(self.path.split('/')[:-1])
            self.ftp.cd(self.path)
            self.cdToParentButton.setEnabled(True)
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
        #self.statusLabel.setText("Connecting to ftp server %s..." % self.ftpServerLabel.text())

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
                    "Unable to connect to the ftp server at %s. Please "
                    "check that the host name is correct." % self.ftpServerLabel.text())
                self.connectOrDisconnect()
                return

            # self.statusLabel.setText("Logged onto %s." % self.ftpServerLabel.text())
            self.fileList.setFocus()
            self.ftp.list()
            self.outFile = None
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
