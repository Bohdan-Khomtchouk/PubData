#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 Bohdan Khomtchouk, Thor Wahlestedt, Kelly Khomtchouk, Kasra Ahmadvand, and Claes Wahlestedt

# This is a GUI version for BioNetHub command line interface, written with PySide.

# BioNetHub is a software program written in the Python programming language that can remotely access, search, and
# navigate through the directory tree of any major bioinformatics database via a local computer network.
# By assembling all major bioinformatics databases under the roof of one software program, BioNetHub allows the user to avoid
# the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using
# an Internet browser. As such, BioNetHub allows researchers to search, access, view, and download files from the FTP
# servers of any major bioinformatics database directly from one centralized location. By using only a command-line environment
# (e.g., Terminal), BioNetHub allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the
# comfort of their local computer. BioNetHub is designed with network programming algorithms that can patch into any
# user-specified bioinformatics online database to be able to search, navigate, view, and download files directly from the command-line
# from one centralized location on a local computer network.


# BioNetHub is an ongoing bioinformatics software project fully financially supported by the
# United States Department of Defense (DoD) through the National Defense Science and Engineering
# Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under
# and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering
# Graduate (NDSEG) Fellowship, 32 CFR 168a.

# Please cite: "Khomtchouk et al.: 'BioNetHub: Python network programming engine for surfing the FTP servers of bioinformatics
# databases', 2015 (in preparation)" within any source that makes use of any methods
# inspired by BioNetHub.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ftplib
import json
import os
import re
import socket
from Queue import Queue
from itertools import chain
from threading import Thread

from PyQt4.QtCore import pyqtSlot

from PySide import QtCore, QtGui, QtNetwork

from nltk.corpus import wordnet

from pymongo import MongoClient

from pymongo.errors import ConnectionFailure


SERVER_NAMES = {'Ensembl Genome Browser': 'ftp_walker_insp.ensembl.org',
                'UCSC Genome Browser': 'hgdownload.cse.ucsc.edu',
                'Uniprot': 'ftp_walker_insp.uniprot.org',
                'Flybase': 'ftp_walker_insp.flybase.net',
                'Xenbase': 'ftp_walker_insp.xenbase.org',
                'The Arabidopsis Information Resource': 'ftp_walker_insp.arabidopsis.org/home',
                'Rat Genome Database': 'rgd.mcw.edu',
                'Human Microbiome Project': 'public-ftp_walker_insp.hmpdacc.org',
                'National Center for Biotechnology Information': 'ftp_walker_insp.ncbi.nlm.nih.gov',
                'REBASE': 'ftp_walker_insp.neb.com',
                'NECTAR': 'ftp_walker_insp.nectarmutation.org',
                'Global Proteome Machine and Database': 'ftp_walker_insp.thegpm.org',
                'Protein Information Resource': 'ftp_walker_insp.pir.georgetown.edu',
                'O-GLYCBASE': 'ftp_walker_insp.cbs.dtu.dk',
                'Pasteur Insitute': 'ftp_walker_insp.pasteur.fr',
                'miRBase': 'mirbase.org',
                'Genomicus': 'ftp_walker_insp.biologie.ens.fr',
                'AAindex': 'ftp_walker_insp.genome.jp',
                'PairsDB': 'nic.funet.fi',
                'Molecular INTeraction database': 'mint.bio.uniroma2.it',
                'PANTHER': 'ftp_walker_insp.pantherdb.org'}


class Edit_servers(QtGui.QDialog):
    """
    ==============
    ``Edit_servers``
    ----------
    .. py:class:: Edit_servers()
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
        super(Edit_servers, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.h_layout = QtGui.QHBoxLayout()
        self.main_layout.insertLayout(0, self.h_layout)

        self.list_a = QtGui.QTreeWidget()
        self.list_a.setHeaderLabels(['Server Names'])
        self.dialog_box = QtGui.QInputDialog()
        with open('SERVER_NAMES.json') as f:
                self.servers = json.load(f)

        for i in self.servers:
            item = QtGui.QTreeWidgetItem()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            item.setText(0, i)
            self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)

        self.self.button_group_box = QtGui.QGroupBox()
        self.button_layout = QtGui.QVBoxLayout()
        self.self.button_group_box.setLayout(self.button_layout)

        get_data_button = QtGui.QPushButton('Add new server')
        get_data_button.clicked.connect(self.addnew)
        self.button_layout.addWidget(get_data_button)

        ok_button = QtGui.QPushButton('Remove Selected')
        ok_button.clicked.connect(self.removeSel)
        self.button_layout.addWidget(ok_button)

        self.main_layout.addWidget(self.self.button_group_box)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

        self.list_a.itemDoubleClicked.connect(self.doubleClickedSlot)

    def itemadder(self, name):
        """
        .. py:attribute:: itemadder()
           :param name:
           :type name:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        item = QtGui.QTreeWidgetItem()
        item.setCheckState(0, QtCore.Qt.Unchecked)
        item.setText(0, name)
        self.list_a.addTopLevelItem(item)
        self.h_layout.addWidget(self.list_a)

    @pyqtSlot(QtGui.QTreeWidget)
    def doubleClickedSlot(self, item):
        """
        .. py:attribute:: doubleClickedSlot()
           :param item:
           :type item:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        current_name = item.text(0)
        name, ok = self.dialog_box.getText(self,
                                           "Edit Servername!",
                                           "Edit the name : {}".format(current_name))
        if ok:

            address, ok = self.dialog_box.getText(self,
                                                  "Edit Server Adress!",
                                                  "Edit the Adress : {}".format(self.servers[current_name]))
            if ok:
                del self.servers[current_name]
                self.servers[name] = address
                item_index = self.list_a.indexOftp_walker_insopLevelItem(item)
                self.list_a.takeTopLevelItem(item_index)
                self.itemadder(name)
                with open('SERVER_NAMES.json', 'w') as f:
                    json.dump(self.servers, f, indent=4)


    def removeSel(self):
        """
        .. py:attribute:: removeSel()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        checked_items = set()
        list_items = self.list_a.invisibleRootItem()
        child_count = list_items.childCount()
        if not list_items:
            return
        for i in range(child_count):
            item = list_items.child(i)
            if item.checkState(0) == QtCore.Qt.CheckState.Checked:
                checked_items.add(item)
        names = [i.text(0) for i in checked_items]
        for item in checked_items:
            item_index = self.list_a.indexOftp_walker_insopLevelItem(item)
            self.list_a.takeTopLevelItem(item_index)


    def addnew(self):
        """
        .. py:attribute:: addnew()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        name, ok = self.dialog_box.getText(self,
                                           "Add Servername!",
                                           "Add the name")
        if ok:
            address, ok = self.dialog_box.getText(self,
                                                  "Add Server Adress!",
                                                  "Add the Adress")
            if ok:
                self.servers[name] = address
                self.itemadder(name)
                with open('SERVER_NAMES.json', 'w') as f:
                    json.dump(self.servers, f, indent=4)


class Sub_path(QtGui.QDialog):
    """
    ==============
    ``Sub_path``
    ----------
    .. py:class:: Sub_path()
       :param :
       :type :
       :rtype: UNKNOWN
    .. note::
    .. todo::
    """
    def __init__(self, root, path, parent=None):
        """
        .. py:attribute:: __init__()
           :param root:
           :type root:
           :param path:
           :type path:
           :param parent:
           :type parent:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        super(Sub_path, self).__init__(parent)
        self.root = root
        self.path = path
        self.isDirectory = {}
        self.ftp_walker_insp = None
        self.outFile = None
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("ftp_walker_insP name : ")
        self.senameLabel.setText(root)
        self.ftp_walker_inspServerLabel = QtGui.QLabel('...')
        self.ftp_walker_inspServerLabel.setFrameStyle(frame_style)

        # self.statusLabel = QtGui.QLabel("Please select the name of an ftp_walker_insP server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.downloadButton = QtGui.QPushButton("Download")
        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon('images/cdtoparent.png'))
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

        self.setWindowTitle("BioNetHub")
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}
        QTextEdit{background-color:#ffffff; color:#000000}QInputDialog{border-radius:4px;color :black;font-weight:500; font-size: 12pt}""")
        self.connectOrDisconnect()


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
        if not self.ftp_walker_insp:
            print 'ceate new ftp_walker_insp'
            self.ftp_walker_insp = QtNetwork.QFtp(self)

        self.setCursor(QtCore.Qt.WaitCursor)
        self.ftp_walker_insp.commandFinished.connect(self.ftp_walker_inspCommandFinished)
        self.ftp_walker_insp.listInfo.connect(self.addToList)
        self.ftp_walker_insp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()
        print self.path
        url = QtCore.QUrl(self.root)
        if not url.isValid() or url.scheme().lower() != 'ftp_walker_insp':
            self.ftp_walker_insp.connectToHost(self.root, 21)
            self.ftp_walker_insp.login()
            self.setCursor(QtCore.Qt.WaitCursor)
            self.fileList.clear()
            self.currentPath = '/'.join(self.path.split('/')[:-1])
            self.ftp_walker_insp.cd(self.path)
            # self.ftp_walker_insp.list()
            self.cdToParentButton.setEnabled(True)
        else:
            self.ftp_walker_insp.connectToHost(url.host(), url.port(21))

            user_name = url.userName()
            if user_name:
                try:
                    # Python v3.
                    user_name = bytes(user_name, encoding='utf-8')
                except:
                    # Python v2.
                    pass

                self.ftp_walker_insp.login(QtCore.QUrl.fromPercentEncoding(user_name), url.password())
            else:
                self.ftp_walker_insp.login()

            if url.path():
                self.ftp_walker_insp.cd(url.path())

        self.fileList.setEnabled(True)
        #self.statusLabel.setText("Connecting to ftp_walker_insP server %s..." % self.ftp_walker_inspServerLabel.text())

    def ftp_walker_inspCommandFinished(self, _, error):
        """
        .. py:attribute:: ftp_walker_inspCommandFinished()
           :param _:
           :type _:
           :param error:
           :type error:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.setCursor(QtCore.Qt.ArrowCursor)

        if self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(
                    self,
                    "ftp_walker_insP",
                    "Unable to connect to the ftp_walker_insP server at %s. Please "
                    "check that the host name is correct." % self.ftp_walker_inspServerLabel.text())
                self.connectOrDisconnect()
                return

            # self.statusLabel.setText("Logged onto %s." % self.ftp_walker_inspServerLabel.text())
            self.fileList.setFocus()
            self.ftp_walker_insp.list()
            self.outFile = None
            self.progressDialog.hide()
        elif self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.List:
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
            icon = QtGui.QIcon('images/dir.png')
        else:
            icon = QtGui.QIcon('images/file.png')
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
            self.ftp_walker_insp.cd(name)
            self.ftp_walker_insp.list()
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
            self.ftp_walker_insp.cd(self.currentPath)
            self.cdToParentButton.setEnabled(False)
        else:
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp_walker_insp.cd(self.currentPath)

        self.ftp_walker_insp.list()

    def change_path(self, path):
        """
        .. py:attribute:: change_path()
           :param path:
           :type path:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.ftp_walker_insp = QtNetwork.QFtp(self)
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.ftp_walker_insp.cd(path)
        self.ftp_walker_insp.list()

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
                "ftp_walker_insP",
                "There already exists a file called %s in the current "
                "directory." % file_name)
            return

        self.outFile = QtCore.QFile(file_name)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(
                self,
                "ftp_walker_insP",
                "Unable to save the file %s: %s." % (file_name, self.outFile.errorString()))
            self.outFile = None
            return

        print self.fileList.currentItem().text(0)
        self.ftp_walker_insp.get(self.fileList.currentItem().text(0), self.outFile)

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
        self.ftp_walker_insp.abort()

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
        self.list_a.setHeaderLabels(['Matched Paths', 'Server name'])
        self.dialog_box = QtGui.QInputDialog()
        for s_name, all_path in self.total_find.items():
            for p in all_path:
                item = QtGui.QTreeWidgetItem()
                item.setText(0, p)
                item.setText(1, s_name)
                self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

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
        self.wind.setWindowTitle('Sub Path')
        self.wind.show()

class SelectServers(QtGui.QDialog):    
    """
    ==============
    ``SelectServers``
    ----------
    .. py:class:: SelectServers()
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
        super(SelectServers, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.selected_SERVER_NAMES = []
        self.h_layout = QtGui.QHBoxLayout()
        self.main_layout.insertLayout(0, self.h_layout)

        self.list_a = QtGui.QTreeWidget()
        self.list_a.setHeaderLabels(['Server Names', 'Exists in DB'])
        self.dialog_box = QtGui.QInputDialog()
        with open('SERVER_NAMES.json')as f:
                self.servers = json.load(f)

        for i in self.servers:
            item = QtGui.QTreeWidgetItem()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            item.setText(0, i)
            if i in COLLECTION_NAMES:
                item.setText(1, 'YES')
            else:
                item.setText(1, 'NO')
                item.setDisabled(True)
            self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)

        self.button_group_box = QtGui.QGroupBox()
        self.button_layout = QtGui.QVBoxLayout()
        self.button_group_box.setLayout(self.button_layout)

        self.ok_button = QtGui.QPushButton('OK')
        self.ok_button.clicked.connect(self.get_selected_servers)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.button_group_box)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

    def get_selected_servers(self):
        """
        .. py:attribute:: get_selected_servers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        checked_items = set()
        list_items = self.list_a.invisibleRootItem()
        child_count = list_items.childCount()
        if not list_items:
            return
        for i in range(child_count):
            item = list_items.child(i)
            if item.checkState(0) == QtCore.Qt.CheckState.Checked:
                checked_items.add(item)
        self.selected_SERVER_NAMES = [i.text(0) for i in checked_items]
        self.close()


class ftp_walker_inspWalker(object):
    """
    ==============
    ``ftp_walker_inspWalker``
    ----------
    .. py:class:: ftp_walker_inspWalker()
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
        conn = ftplib.ftp_walker_insP(self.servername)
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
        connection = ftp_walker_insP(self.servername)
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


class ftp_walker_inspWindow(QtGui.QDialog):
    """
    ==============
    ``ftp_walker_inspWindow``
    ----------
    .. py:class:: ftp_walker_inspWindow()
       :param :
       :type :
       :rtype: UNKNOWN
    .. note::
    .. todo::
    """
    def __init__(self, SelectServers=None, parent=None):
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
        super(ftp_walker_inspWindow, self).__init__(parent)
        self.dbname = "BioNetHub"
        self.mongo_cursor = self.mongo_connector()
        self.collection_names = self.mongo_cursor.collection_names()
        if SelectServers:
            self.Select_s = SelectServers()
            self.Select_s.ok_button.clicked.connect(self.put_get_servers)
        self.isDirectory = {}
        self.ftp_walker_insp = None
        self.outFile = None
        self.SERVER_NAMES = self.getServerNames()
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("ftp_walker_insP name : ")
        self.ftp_walker_inspServerLabel = QtGui.QLabel('...')
        self.ftp_walker_inspServerLabel.setFrameStyle(frame_style)

        self.statusLabel = QtGui.QLabel("Please select the name of an ftp_walker_insP server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.setDefault(True)

        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon('images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)

        self.serverButton = QtGui.QPushButton('server list')
        self.downloadButton = QtGui.QPushButton("Download")
        self.downloadButton.setEnabled(False)

        self.addserverButton = QtGui.QPushButton("Add server to search")

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialog_box = QtGui.QInputDialog()

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialog_box = QtGui.QInputDialog()

        self.EditserverButton = QtGui.QPushButton("Editservers")
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
        top_layout.addWidget(self.ftp_walker_inspServerLabel)
        top_layout.addWidget(self.serverButton)
        top_layout.addWidget(self.cdToParentButton)
        top_layout.addWidget(self.connectButton)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.fileList)
        main_layout.addWidget(self.statusLabel)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        self.setWindowTitle("BioNetHub")
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}
        QTextEdit{background-color:#ffffff; color:#000000}QInputDialog{border-radius:4px;color :black;font-weight:500; font-size: 12pt}""")

    def getServerNames(self):
        """
        .. py:attribute:: getServerNames()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        try:
            with open('SERVER_NAMES.json')as f:
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
                                              "Season:",
                                              self.SERVER_NAMES.keys(),
                                              0,
                                              False)
        if ok and item:
            self.ftp_walker_inspServerLabel.setText(self.SERVER_NAMES[item])
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
        # self.ftp_walker_inspServerLabel.text() = self.selected_SERVER_NAMES.pop(0)
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
                                              self.SERVER_NAMES.keys(),
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
            ftp_walker_ins = ftp_walker_inspWalker(self.SERVER_NAMES[name])
            ftp_walker_ins.run()
        except ftplib.error_temp as e:
            self.statusLabel.setText("Update Failed")
            QtGui.QMessageBox.error(self,
                                    "QMessageBox.information()",
                                    e)
        except ftplib.error_perm as e:
            self.statusLabel.setText("Update Failed")
            QtGui.QMessageBox.error(self,
                                    "QMessageBox.information()",
                                    e)
        except socket.gaierror as e:
            self.statusLabel.setText("Update Failed")
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
        self.wid = Edit_servers()
        self.wid.resize(350, 650)
        self.wid.setWindowTitle('NewWindow')
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
        if self.ftp_walker_insp:
            self.ftp_walker_insp.abort()
            self.ftp_walker_insp.deleteLater()
            self.ftp_walker_insp = None

            self.fileList.setEnabled(False)
            self.cdToParentButton.setEnabled(False)
            self.downloadButton.setEnabled(False)
            self.connectButton.setEnabled(True)
            self.connectButton.setText("Connect")
            self.setCursor(QtCore.Qt.ArrowCursor)

            return

        self.setCursor(QtCore.Qt.WaitCursor)

        self.ftp_walker_insp = QtNetwork.QFtp(self)
        self.ftp_walker_insp.commandFinished.connect(self.ftp_walker_inspCommandFinished)
        self.ftp_walker_insp.listInfo.connect(self.addToList)
        self.ftp_walker_insp.dataTransferProgress.connect(self.updateDataTransferProgress)

        self.fileList.clear()
        self.currentPath = ''
        self.isDirectory.clear()

        url = QtCore.QUrl(self.ftp_walker_inspServerLabel.text())
        if not url.isValid() or url.scheme().lower() != 'ftp_walker_insp':
            self.ftp_walker_insp.connectToHost(self.ftp_walker_inspServerLabel.text(), 21)
            self.ftp_walker_insp.login()
        else:
            self.ftp_walker_insp.connectToHost(url.host(), url.port(21))

            user_name = url.userName()
            if user_name:
                try:
                    # Python v3.
                    user_name = bytes(user_name, encoding='utf-8')
                except:
                    # Python v2.
                    pass

                self.ftp_walker_insp.login(QtCore.QUrl.fromPercentEncoding(user_name), url.password())
            else:
                self.ftp_walker_insp.login()

            if url.path():
                self.ftp_walker_insp.cd(url.path())

        self.fileList.setEnabled(True)
        self.connectButton.setEnabled(False)
        self.connectButton.setText("Disconnect")
        self.statusLabel.setText("Connecting to ftp_walker_insP server %s..." % self.ftp_walker_inspServerLabel.text())

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
                "ftp_walker_insP",
                "There already exists a file called %s in the current "
                "directory." % file_name)
            return

        self.outFile = QtCore.QFile(file_name)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(
                self,
                "ftp_walker_insP",
                "Unable to save the file %s: %s." % (file_name, self.outFile.errorString()))
            self.outFile = None
            return

        print self.fileList.currentItem().text(0)
        self.ftp_walker_insp.get(self.fileList.currentItem().text(0), self.outFile)

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
        self.ftp_walker_insp.abort()

    def ftp_walker_inspCommandFinished(self, _, error):
        """
        .. py:attribute:: ftp_walker_inspCommandFinished()
           :param _:
           :type _:
           :param error:
           :type error:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.setCursor(QtCore.Qt.ArrowCursor)
        if self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(
                    self,
                    "ftp_walker_insP",
                    "Unable to connect to the ftp_walker_insP server at %s. Please "
                    "check that the host name is correct." % self.ftp_walker_inspServerLabel.text())
                self.connectOrDisconnect()
                return

            self.statusLabel.setText("Logged onto %s." % self.ftp_walker_inspServerLabel.text())
            self.fileList.setFocus()
            self.downloadButton.setDefault(True)
            self.connectButton.setEnabled(True)
            return

        if self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.Login:
            self.ftp_walker_insp.list()

        if self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.Get:
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
        elif self.ftp_walker_insp.currentCommand() == QtNetwork.QFtp.List:
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
            icon = QtGui.QIcon('images/dir.png')
        else:
            icon = QtGui.QIcon('images/file.png')
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
            self.ftp_walker_insp.cd(name)
            self.ftp_walker_insp.list()
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
            self.ftp_walker_insp.cd(self.currentPath)
            self.cdToParentButton.setEnabled(False)
        else:
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp_walker_insp.cd(self.currentPath)

        self.ftp_walker_insp.list()

    def change_path(self, path):
        """
        .. py:attribute:: change_path()
           :param path:
           :type path:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.ftp_walker_insp = QtNetwork.QFtp(self)
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.ftp_walker_insp.cd(path)
        self.ftp_walker_insp.list()

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
        text, ok = self.dialog_box.getText(QtGui.QInputDialog(), "Search for file",'Enter the name of your file ',QtGui.QLineEdit.Normal)
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
                    self.wid = Path_results(self.SERVER_NAMES, total_find, match_path_number)
                    self.wid.resize(350, 650)
                    self.wid.setWindowTitle('NewWindow')
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
                # self.regural_search(text,self.servername,self.ftp_walker_inspServerLabel.text())

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

    def regural_search(self, word, ftp_walker_insp, severname, sever_url):
        """
        .. py:attribute:: regural_search()
           :param word:
           :type word:
           :param ftp_walker_insp:
           :type ftp_walker_insp:
           :param severname:
           :type severname:
           :param sever_url:
           :type sever_url:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        try:
            ftp_walker_ins = ftp_walker_insp_walker(j)
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
                self.wid = Path_results(ftp_walker_insp, paths, servername)
                self.wid.resize(350, 650)
                self.wid.setWindowTitle('NewWindow')
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
        self.Select_s.setWindowTitle('Select server')
        self.Select_s.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ftp_walker_inspWin_ = ftp_walker_inspWindow()
    COLLECTION_NAMES = ftp_walker_inspWin_.collection_names
    selected_s = SelectServers
    ftp_walker_inspWin = ftp_walker_inspWindow(selected_s)
    COLLECTION_NAMES = ftp_walker_inspWin.collection_names
    ftp_walker_inspWin.show()
    sys.exit(ftp_walker_inspWin.exec_())
