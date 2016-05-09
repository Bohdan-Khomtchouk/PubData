#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------


# -*- coding: utf-8 -*-


import json
import re
from itertools import chain
from extras import general_style
from PyQt4.QtCore import pyqtSlot
from PySide import QtCore, QtGui, QtNetwork
from nltk.corpus import wordnet
from searchpath import Path_results
from editserver import Edit_servers
from selectservers import SelectServers
import sqlite3 as lite
from updateservers import MainUpdate
from ast import literal_eval

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
           :param parent:
           :type parent:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        super(ftpWindow, self).__init__(parent)
        self.dbname = "PubData"
        self.createMenu()
        self.server_dict, self.server_names = self.getServerNames()
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.select_s = SelectServers(self.server_names)
        self.select_s.ok_button.clicked.connect(self.put_get_servers)

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
        button_box.addButton(self.downloadButton, QtGui.QDialogButtonBox.ActionRole)

        self.progressDialog = QtGui.QProgressDialog(self)
        self.fileList.itemActivated.connect(self.processItem)
        self.fileList.currentItemChanged.connect(self.enableDownloadButton)
        self.progressDialog.canceled.connect(self.cancelDownload)
        self.connectButton.clicked.connect(self.connectOrDisconnect)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        self.serverButton.clicked.connect(self.select)

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
        main_layout.setMenuBar(self.menuBar)
        self.setLayout(main_layout)
        self.setWindowTitle("PubData")
        self.setStyleSheet(general_style)

    def createMenu(self):
        self.menuBar = QtGui.QMenuBar()

        self.fileMenu1 = QtGui.QMenu("&File", self)
        self.server_list_action = self.fileMenu1.addAction("Server list")
        self.exit_action = self.fileMenu1.addAction("Exit")
        self.exit_action.setShortcut('Ctrl+E')
        self.exit_action.setStatusTip('Exit application')
        self.fileMenu2 = QtGui.QMenu("&Action", self)
        self.edit_servers_action = self.fileMenu2.addAction("Edit servers")
        self.update_all_action = self.fileMenu2.addAction("Update all")
        self.update_manual_action = self.fileMenu2.addAction("Update manual")

        self.fileMenu3 = QtGui.QMenu("&Search", self)
        self.manual_search_action = self.fileMenu3.addAction("Manual search")
        self.search_all_action = self.fileMenu3.addAction("Search in all databases")

        self.fileMenu4 = QtGui.QMenu("&Help", self)
        self.help_action = self.fileMenu4.addAction("Help")
        self.about_ction = self.fileMenu4.addAction("About us")

        self.menuBar.addMenu(self.fileMenu1)
        self.menuBar.addMenu(self.fileMenu2)
        self.menuBar.addMenu(self.fileMenu3)
        self.menuBar.addMenu(self.fileMenu4)

        self.server_list_action.triggered.connect(self.select)
        self.exit_action.triggered.connect(self.close)

        self.edit_servers_action.triggered.connect(self.editservers)
        self.update_all_action.triggered.connect(self.update_servers_all)
        self.update_manual_action.triggered.connect(self.update_servers_manual)

        self.manual_search_action.triggered.connect(self.manual_search)
        self.search_all_action.triggered.connect(self.search_all)

        # self.help_action.triggered.connect()
        # self.about_list_action.triggered.connect()

    def getServerNames(self):
        """
        .. py:attribute:: getServerNames()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        with open('data/SERVER_NAMES.json')as f:
            d = json.load(f)
            return d, d.keys()

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
                                              self.server_names,
                                              0,
                                              False)
        if ok and item:
            self.ftpServerLabel.setText(self.server_dict[item])
            self.servername = item

    def update_servers_all(self):
        """
        .. py:attribute:: update_servers_all()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.statusLabel.setText("Start updating ...")
        mu = MainUpdate()
        mu.update_all()

    def update_servers_manual(self):
        self.statusLabel.setText("Start updating ...")
        selected_server_names = self.Select_s.selected_SERVER_NAMES
        mu = MainUpdate(manual_list=selected_server_names)
        mu.update_manual()

    def editservers(self):
        """
        .. py:attribute:: editservers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.wid = Edit_servers(self.server_names)
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
        return QtCore.QSize(900, 400)

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

    @pyqtSlot(QtGui.QTreeWidget)
    def put_get_servers(self):
        selected_names = self.select_s.selected_server_names
        self.search(selected_names)
        self.statusLabel.setText("Search in servers...")

    def manual_search(self):
        self.select_s.resize(350, 650)
        self.select_s.setWindowTitle('Select server names for search')
        self.select_s.show()

    def search_all(self):
        self.statusLabel.setText("Search in servers...")
        self.search(self.server_names)

    def search(self, server_names):
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
            words = self.cal_regex(text)
            total_find = {}
            match_path_number = 0
            try:
                conn = lite.connect('../database/PubData.db')
                # conn.row_factory = lambda cursor, row: row[0]
                cursor = conn.cursor()
            except Exception as exp:
                print exp
            else:
                for servername in server_names:
                        # conn.create_function("REGEXP", 2, self.cal_regex)
                        t_name = '_'.join(map(unicode.lower, servername.split()))
                        items = [i for j in zip(words, words) for i in j]
                        str_query = "OR file_name like '%{}%' OR file_path like '%{}%' " * len(words)
                        str_query = str_query.format(*items)
                        try:
                            query = """SELECT file_path FROM {} WHERE file_name like '%{}%'
                                                                OR    file_path like '%{}%'
                                                                {}""".format(t_name, text, text, str_query)
                            cursor.execute(query)
                            rows = {i[0] for i in cursor.fetchall()}
                        except Exception as exp:
                            print exp
                        else:
                            total_find[servername] = rows
                            match_path_number += len(rows)
                if match_path_number:
                    self.wid = Path_results(self.server_dict, total_find, match_path_number)
                    self.wid.resize(350, 650)
                    self.wid.setWindowTitle('Search')
                    self.wid.show()
                else:
                    message = """<p>No results.<p>Please try with another pattern.</p>"""
                    QtGui.QMessageBox.information(self, "QMessageBox.information()", message)

    def cal_regex(self, text):
        """
        .. py:attribute:: cal_regex()
           :param text:
           :type text:
            :rtype: UNKNOWN
        .. note::
        """
        print "cal_regex"
        all_text = re.split(r'\W', text)
        synonyms = set(chain.from_iterable([wordnet.synsets(i) for i in all_text]))
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        # lemmas = self.get_wordnet_words(text).union(lemmas)
        self.statusLabel.setText("Search into selected databases. Please wait...")
        return lemmas

    def get_wordnet_words(self, text):
        conn = lite.connect('../database/PubData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM wordnet WHERE word like '%{}%';".format(text))
        seen = set()
        try:
            for row in cursor.fetchall():
                for _, w, syns in row:
                    seen |= set(literal_eval(syns))|{w}
        except Exception as exp:
            print 'Exception: ', str(exp)
            return set()
        else:
            return seen

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
    ftpWin = ftpWindow()
    ftpWin.resize(950, 600)
    ftpWin.show()
    sys.exit(ftpWin.exec_())
