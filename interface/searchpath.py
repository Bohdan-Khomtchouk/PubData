#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------
from PySide import QtCore, QtGui, QtNetwork
import sys
import os
from PyQt4.QtCore import pyqtSlot
from extras.extras import general_style
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.Metafiles import Meta


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
        name = item.text(1)
        print("selected server_name is : {} The address is {} ".format(name, self.SERVER_NAMES[name]))
        self.wind = Sub_path(self.SERVER_NAMES[name], item.text(0), item.text(1))
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
    def __init__(self, root, path, name, parent=None):
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
        self.metainstance = Meta(name)
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
        self.downloadButton2 = QtGui.QPushButton("Metadata")
        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon('images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)

        self.progressDialog = QtGui.QProgressDialog(self)

        self.fileList.itemActivated.connect(self.processItem)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.downloadButton2.clicked.connect(self.show_metadata)

        button_box = QtGui.QDialogButtonBox()
        button_box.addButton(self.downloadButton, QtGui.QDialogButtonBox.ActionRole)
        button_box.addButton(self.downloadButton2, QtGui.QDialogButtonBox.ActionRole)
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
            print('create new FTP connection')
            self.ftp = QtNetwork.QFtp(self)

        self.setCursor(QtCore.Qt.WaitCursor)
        self.ftp.commandFinished.connect(self.ftpCommandFinished)
        self.ftp.listInfo.connect(self.addToList)
        self.ftp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()
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

    def show_metadata(self):
        self.metainstance.setWindowTitle("Meta files")
        self.metainstance.resize(640, 480)
        self.metainstance.show()