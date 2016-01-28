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

from PySide import QtCore, QtGui, QtNetwork
import json
import ftp_rc
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
import ftplib
from os import path
from threading import Thread
from Queue import Queue
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
from nltk.corpus import wordnet
from itertools import chain
import re

SERVER_NAMES={'Ensembl Genome Browser':'ftp.ensembl.org',
'UCSC Genome Browser':'hgdownload.cse.ucsc.edu',
'Uniprot':'ftp.uniprot.org',
'Flybase':'ftp.flybase.net',
'Xenbase':'ftp.xenbase.org',
'The Arabidopsis Information Resource':'ftp.arabidopsis.org/home',
'Rat Genome Database':'rgd.mcw.edu',
'Human Microbiome Project':'public-ftp.hmpdacc.org',
'National Center for Biotechnology Information':'ftp.ncbi.nlm.nih.gov',
'REBASE':'ftp.neb.com',
'NECTAR':'ftp.nectarmutation.org',
'Global Proteome Machine and Database':'ftp.thegpm.org',
'Protein Information Resource':'ftp.pir.georgetown.edu',
'O-GLYCBASE':'ftp.cbs.dtu.dk',
'Pasteur Insitute':'ftp.pasteur.fr',
'miRBase':'mirbase.org',
'Genomicus':'ftp.biologie.ens.fr',
'AAindex':'ftp.genome.jp',
'PairsDB':'nic.funet.fi',
'Molecular INTeraction database':'mint.bio.uniroma2.it',
'PANTHER':'ftp.pantherdb.org'}

class Edit_servers(QtGui.QDialog):    
    def __init__(self,parent=None):
        super(Edit_servers, self).__init__(parent)                
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.hLayout = QtGui.QHBoxLayout()
        self.mainLayout.insertLayout(0, self.hLayout)

        self.listA=QtGui.QTreeWidget()
        self.listA.setHeaderLabels(['Server Names'])
        self.dialogbox=QtGui.QInputDialog()
        with open('SERVER_NAMES.json')as f:
                self.servers=json.load(f)
        
        for i in self.servers:    
            item=QtGui.QTreeWidgetItem()
            item.setCheckState(0,QtCore.Qt.Unchecked)
            item.setText(0, i)
            self.listA.addTopLevelItem(item)

        self.hLayout.addWidget(self.listA)

        self.buttonGroupbox = QtGui.QGroupBox()
        self.buttonlayout = QtGui.QVBoxLayout()
        self.buttonGroupbox.setLayout(self.buttonlayout)

        getDataButton = QtGui.QPushButton('Add new server')
        getDataButton.clicked.connect(self.addnew)
        self.buttonlayout.addWidget(getDataButton)

        okButton = QtGui.QPushButton('Remove Selected')
        okButton.clicked.connect(self.removeSel)
        self.buttonlayout.addWidget(okButton)

        self.mainLayout.addWidget(self.buttonGroupbox)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

        self.listA.itemDoubleClicked.connect(self.doubleClickedSlot)


    def itemadder(self,name):    
        item=QtGui.QTreeWidgetItem()
        item.setCheckState(0,QtCore.Qt.Unchecked)
        item.setText(0, name)
        self.listA.addTopLevelItem(item)
        self.hLayout.addWidget(self.listA)

    @pyqtSlot(QtGui.QTreeWidget)
    def doubleClickedSlot(self,item):
        current_name=item.text(0)
        name,ok=self.dialogbox.getText(self,
                  "Edit Servername!",
                  "Edit the name : {}".format(current_name))
        if ok:

            address,ok=self.dialogbox.getText(self,
                  "Edit Server Adress!",
                  "Edit the Adress : {}".format(self.servers[current_name]))
            if ok:
                del self.servers[current_name]
                self.servers[name]=address
                itemIndex=self.listA.indexOfTopLevelItem(item)
                self.listA.takeTopLevelItem(itemIndex)
                self.itemadder(name)
                with open('SERVER_NAMES.json','w') as f:
                    json.dump(self.servers,f,indent=4)


    def removeSel(self):
        checked_items=set()
        listItems=self.listA.invisibleRootItem()
        child_count = listItems.childCount()
        if not listItems: return   
        for i in range(child_count):
            item = listItems.child(i)
            if item.checkState(0)==QtCore.Qt.CheckState.Checked:
                checked_items.add(item)
        names = [i.text(0) for i in checked_items]
        for item in checked_items:
            itemIndex=self.listA.indexOfTopLevelItem(item)
            self.listA.takeTopLevelItem(itemIndex)
                

    def addnew(self):
        name,ok=self.dialogbox.getText(self,
                  "Add Servername!",
                  "Add the name")
        if ok:
            address,ok=self.dialogbox.getText(self,
                  "Add Server Adress!",
                  "Add the Adress")
            if ok:
                self.servers[name]=address
                self.itemadder(name)
                with open('SERVER_NAMES.json','w') as f:
                    json.dump(self.servers,f,indent=4)


class Sub_path(QtGui.QDialog):
    def __init__(self,root, path, parent=None):
        super(Sub_path, self).__init__(parent)
        self.root = root
        self.path = path
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("FTP name : ")
        self.senameLabel.setText(root)
        self.ftpServerLabel = QtGui.QLabel('...')
        self.ftpServerLabel.setFrameStyle(frameStyle)

        #self.statusLabel = QtGui.QLabel("Please select the name of an FTP server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.downloadButton = QtGui.QPushButton("Download")
        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon(':/images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)
        
        self.progressDialog = QtGui.QProgressDialog(self)

        self.fileList.itemActivated.connect(self.processItem)
        self.cdToParentButton.clicked.connect(self.cdToParent)
        self.downloadButton.clicked.connect(self.downloadFile)
        
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,QtGui.QDialogButtonBox.ActionRole)
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.senameLabel)
        topLayout.addWidget(self.cdToParentButton)
        
        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.fileList)
        #mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("BioNetHub")
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}
        QTextEdit{background-color:#ffffff; color:#000000}QInputDialog{border-radius:4px;color :black;font-weight:500; font-size: 12pt}""")
        self.connectOrDisconnect()


    def sizeHint(self):
        return QtCore.QSize(800, 400)


    def connectOrDisconnect(self):
        if  not self.ftp:
            print 'ceate new ftp'
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
            #self.ftp.list()
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
        #self.statusLabel.setText("Connecting to FTP server %s..." % self.ftpServerLabel.text())

    def ftpCommandFinished(self, _, error):
        self.setCursor(QtCore.Qt.ArrowCursor)

        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self, "FTP",
                        "Unable to connect to the FTP server at %s. Please "
                        "check that the host name is correct." % self.ftpServerLabel.text())
                self.connectOrDisconnect()
                return

            #self.statusLabel.setText("Logged onto %s." % self.ftpServerLabel.text())
            self.fileList.setFocus()
            self.ftp.list()
            self.outFile = None
            self.progressDialog.hide()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            if not self.isDirectory:
                self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem(["<empty>"]))
                self.fileList.setEnabled(False)

    def addToList(self, urlInfo):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, urlInfo.name())
        item.setText(1, str(urlInfo.size()))
        item.setText(2, urlInfo.owner())
        item.setText(3, urlInfo.group())
        item.setText(4, urlInfo.lastModified().toString('MMM dd yyyy'))

        if urlInfo.isDir():
            icon = QtGui.QIcon(':/images/dir.png')
        else:
            icon = QtGui.QIcon(':/images/file.png')
        item.setIcon(0, icon)

        self.isDirectory[urlInfo.name()] = urlInfo.isDir()
        self.fileList.addTopLevelItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.topLevelItem(0))
            self.fileList.setEnabled(True)

    def processItem(self, item):
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
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()

        dirs = self.currentPath.split('/')
        if len(dirs) == 2:
            self.currentPath = '/'
            self.ftp.cd(self.currentPath)
            self.cdToParentButton.setEnabled(False)
        else :
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp.cd(self.currentPath)

        self.ftp.list()
    
    def change_path(self,path):
        self.ftp = QtNetwork.QFtp(self)
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.ftp.cd(path)
        self.ftp.list()

    def updateDataTransferProgress(self, readBytes, totalBytes):
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)

    def enableDownloadButton(self):
        current = self.fileList.currentItem()
        if current:
            currentFile = current.text(0)
            self.downloadButton.setEnabled(not self.isDirectory.get(currentFile))
        else:
            self.downloadButton.setEnabled(False)
    def downloadFile(self):
        fileName = self.fileList.currentItem().text(0)

        if QtCore.QFile.exists(fileName):
            QtGui.QMessageBox.information(self, "FTP",
                    "There already exists a file called %s in the current "
                    "directory." % fileName)
            return

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "FTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        print self.fileList.currentItem().text(0)
        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText("Downloading %s..." % fileName)
        self.downloadButton.setEnabled(False)
        self.progressDialog.exec_()

    def cancelDownload(self):
        self.ftp.abort()

class Path_results(QtGui.QDialog):    
    def __init__(self,server_names, total_find, path_number, parent=None):
        super(Path_results, self).__init__(parent)                
        self.mainLayout = QtGui.QVBoxLayout()
        self.path_number = path_number
        self.setLayout(self.mainLayout)
        self.total_find = total_find
        self.SERVER_NAMES = server_names
        self.hLayout = QtGui.QHBoxLayout()
        self.countLabel = QtGui.QLabel("{} Results founded!".format(self.path_number))
        topLayout = QtGui.QVBoxLayout()
        topLayout.addWidget(self.countLabel)
        self.mainLayout.addLayout(topLayout)
        self.mainLayout.insertLayout(0, self.hLayout)
        self.listA=QtGui.QTreeWidget()
        self.listA.setHeaderLabels(['Matched Paths', 'Server name'])
        self.dialogbox=QtGui.QInputDialog()
        for s_name,all_path in self.total_find.items():
            for p in all_path:
                item=QtGui.QTreeWidgetItem()
                item.setText(0, p)
                item.setText(1, s_name)
                self.listA.addTopLevelItem(item)

        self.hLayout.addWidget(self.listA)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

        self.listA.itemDoubleClicked.connect(self.doubleClicked_path)

    @pyqtSlot(QtGui.QTreeWidget)
    def doubleClicked_path(self,item):
        self.wind = Sub_path(self.SERVER_NAMES[item.text(1)],item.text(0))
        self.wind.resize(450, 650)
        self.wind.setWindowTitle('Sub Path')
        self.wind.show()

class SelectServers(QtGui.QDialog):    
    def __init__(self,parent=None):
        super(SelectServers, self).__init__(parent)                
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.selected_SERVER_NAMES = []
        self.hLayout = QtGui.QHBoxLayout()
        self.mainLayout.insertLayout(0, self.hLayout)

        self.listA=QtGui.QTreeWidget()
        self.listA.setHeaderLabels(['Server Names', 'Exists in DB'])
        self.dialogbox=QtGui.QInputDialog()
        with open('SERVER_NAMES.json')as f:
                self.servers=json.load(f)
        
        for i in self.servers:    
            item=QtGui.QTreeWidgetItem()
            item.setCheckState(0,QtCore.Qt.Unchecked)
            item.setText(0, i)
            if i in COLLECTION_NAMES:
                item.setText(1, 'YES')
            else:
                item.setText(1, 'NO')
                item.setDisabled(True)
            self.listA.addTopLevelItem(item)

        self.hLayout.addWidget(self.listA)

        self.buttonGroupbox = QtGui.QGroupBox()
        self.buttonlayout = QtGui.QVBoxLayout()
        self.buttonGroupbox.setLayout(self.buttonlayout)

        self.okButton = QtGui.QPushButton('OK')
        self.okButton.clicked.connect(self.get_selected_servers)
        self.buttonlayout.addWidget(self.okButton)

        self.mainLayout.addWidget(self.buttonGroupbox)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

    def get_selected_servers(self):
        checked_items=set()
        listItems=self.listA.invisibleRootItem()
        child_count = listItems.childCount()
        if not listItems: return   
        for i in range(child_count):
            item = listItems.child(i)
            if item.checkState(0)==QtCore.Qt.CheckState.Checked:
                checked_items.add(item)
        self.selected_SERVER_NAMES = [i.text(0) for i in checked_items]
        self.close()


class FtpWalker(object):
    def __init__(self,servername):
        self.servername = servername
        self.all_path = Queue()
        self.base,self.leading = self.find_leading()

    def find_leading(self):
        base = []
        conn=ftplib.FTP(self.servername)
        conn.login()
        for p,dirs,files in self.Walk(conn,'/'):
            length = len(dirs)
            base.append((p,files))
            if length > 1 :
                p = '/'.join(p.split('/')[1:])
                return base,[p+'/'+i for i in dirs]

    def listdir(self, connection, _path):
        file_list, dirs, nondirs = [],[],[]
        try:
            connection.cwd(_path)
        except:
            return [],[]

        connection.retrlines('LIST',lambda x:file_list.append(x.split()))
        for info in file_list:
            ls_type,name = info[0],info[-1]
            if ls_type.startswith('d'):
                dirs.append(name)
            else:
                nondirs.append(name)
        return dirs,nondirs

    def Walk(self, connection, top):
        dirs, nondirs = self.listdir(connection,top)
        yield top, dirs, nondirs
        for name in dirs:
            new_path = path.join(top, name)
            for x in self.Walk(connection, new_path):
                yield x

    def Traverse(self, _path='/',word=''):
        connection=ftplib.FTP(self.servername)
        try:
            connection.login()
        except:
            print 'Connection failed for path : ', _path
        else:
            try:
                conn.cwd(path)
            except:
                pass
            else:
                for _path,_,files in self.Walk(connection, _path):
                    if word:
                        if any(word in file_name for file_name in files):
                            self.all_path.put((_path,files))
                    else:
                        self.all_path.put((_path,files))
                
    def run(self, word, threads=[]):
        print 'start threads...'
        mkdir(self.servername)
        for conn in self.leading:
            thread = Thread(target=self.Traverse,args=(conn,word))
            thread.start()
            threads.append(thread)
        for thread in threads:
                thread.join()


class FtpWindow(QtGui.QDialog):
    def __init__(self, SelectServers=None, parent=None):
        super(FtpWindow, self).__init__(parent)
        self.dbname = "BioNetHub"
        self.mongo_cursor = self.mongo_connector()
        self.collection_names = self.mongo_cursor.collection_names()
        if SelectServers:
            self.Select_s = SelectServers()
            self.Select_s.okButton.clicked.connect(self.put_get_servers)
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        self.SERVER_NAMES = self.getServerNames()
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel

        self.senameLabel = QtGui.QLabel("FTP name : ")
        self.ftpServerLabel = QtGui.QLabel('...')
        self.ftpServerLabel.setFrameStyle(frameStyle)

        self.statusLabel = QtGui.QLabel("Please select the name of an FTP server.")

        self.fileList = QtGui.QTreeWidget()
        self.fileList.setEnabled(False)
        self.fileList.setRootIsDecorated(False)
        self.fileList.setHeaderLabels(("Name", "Size", "Owner", "Group", "Time"))
        self.fileList.header().setStretchLastSection(True)

        self.connectButton = QtGui.QPushButton("Connect")
        self.connectButton.setDefault(True)

        self.cdToParentButton = QtGui.QPushButton()
        self.cdToParentButton.setIcon(QtGui.QIcon(':/images/cdtoparent.png'))
        self.cdToParentButton.setEnabled(False)
        
        self.serverButton = QtGui.QPushButton('server list')
        
        self.downloadButton = QtGui.QPushButton("Download")
        self.downloadButton.setEnabled(False)

        self.addserverButton = QtGui.QPushButton("Add server to search")

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialogbox=QtGui.QInputDialog()

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialogbox=QtGui.QInputDialog()
        
        self.EditserverButton = QtGui.QPushButton("Editservers")
        self.UpdateserverButton = QtGui.QPushButton("Update custom servers")
        
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        buttonBox.addButton(self.EditserverButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.UpdateserverButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.downloadButton,QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.addserverButton, QtGui.QDialogButtonBox.ActionRole)


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

        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.senameLabel)
        topLayout.addWidget(self.ftpServerLabel)
        topLayout.addWidget(self.serverButton)
        topLayout.addWidget(self.cdToParentButton)
        topLayout.addWidget(self.connectButton)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.fileList)
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.setWindowTitle("BioNetHub")
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}
        QTextEdit{background-color:#ffffff; color:#000000}QInputDialog{border-radius:4px;color :black;font-weight:500; font-size: 12pt}""")

    def getServerNames(self):
        try:
            with open('SERVER_NAMES.json')as f:
                return json.load(f)
        except IOError:
            with open('SERVER_NAMES.json','w') as f:
                json.dump(SERVER_NAMES,f,indent=4)
                MESSAGE="""<p>Couldn't find the server file.</p>
                <p>Server names has beed rewrite, you can try again.</p>"""
                QtGui.QMessageBox.information(self,
                "QMessageBox.information()", MESSAGE)

    def select(self):
        item, ok = QtGui.QInputDialog.getItem(self, "Select a server name ",
                "Season:", self.SERVER_NAMES.keys(), 0, False)
        if ok and item:
            self.ftpServerLabel.setText(self.SERVER_NAMES[item])
            self.servername = item

    @pyqtSlot(QtGui.QTreeWidget)
    def put_get_servers(self):
        self.selected_SERVER_NAMES = self.Select_s.selected_SERVER_NAMES
        #self.ftpServerLabel.text() = self.selected_SERVER_NAMES.pop(0)
        self.statusLabel.setText("Search in servers: {}".format(','.join(self.selected_SERVER_NAMES)))

    def updateservers(self):
        self.statusLabel.setText("Start updating ...")
        item, ok = QtGui.QInputDialog.getItem(self, "Select a server name ",
                "Season:", self.SERVER_NAMES.keys(), 0, False)
        if ok and item:
            self.updateServerFile(item)

    def queue_traverser(self,queue):
        while queue.qsize() > 0:
            yield queue.get()

    def updateServerFile(self,name):
        try:
            self.statusLabel.setText("Start updating of {} ...".format(name))
            FT=FtpWalker(self.SERVER_NAMES[name])
            FT.run()
        except ftplib.error_temp as e:
            self.statusLabel.setText("Update Failed")
            QtGui.QMessageBox.error(self,
            "QMessageBox.information()", e)
        except ftplib.error_perm as e:
            self.statusLabel.setText("Update Failed")
            QtGui.QMessageBox.error(self,
            "QMessageBox.information()", e)
        except socket.gaierror as e:
            self.statusLabel.setText("Update Failed")
            QtGui.QMessageBox.error(self,
            "QMessageBox.information()", e)
        else:
            for _path, files in queue_traverser(FT.all_path):
                mongo_cursor[self.servername].insert(
                    {
                        'path': _path,
                        'files': files
                    }
                )

    def editservers(self):
        self.wid = Edit_servers()
        self.wid.resize(350, 650)
        self.wid.setWindowTitle('NewWindow')
        self.wid.show()

    def sizeHint(self):
        return QtCore.QSize(800, 400)


    def connectOrDisconnect(self):
        if  self.ftp:
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
        self.statusLabel.setText("Connecting to FTP server %s..." % self.ftpServerLabel.text())

    def downloadFile(self):
        fileName = self.fileList.currentItem().text(0)

        if QtCore.QFile.exists(fileName):
            QtGui.QMessageBox.information(self, "FTP",
                    "There already exists a file called %s in the current "
                    "directory." % fileName)
            return

        self.outFile = QtCore.QFile(fileName)
        if not self.outFile.open(QtCore.QIODevice.WriteOnly):
            QtGui.QMessageBox.information(self, "FTP",
                    "Unable to save the file %s: %s." % (fileName, self.outFile.errorString()))
            self.outFile = None
            return

        print self.fileList.currentItem().text(0)
        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText("Downloading %s..." % fileName)
        self.downloadButton.setEnabled(False)
        self.progressDialog.exec_()

    def cancelDownload(self):
        self.ftp.abort()

    def ftpCommandFinished(self, _, error):
        self.setCursor(QtCore.Qt.ArrowCursor)
        if self.ftp.currentCommand() == QtNetwork.QFtp.ConnectToHost:
            if error:
                QtGui.QMessageBox.information(self, "FTP",
                        "Unable to connect to the FTP server at %s. Please "
                        "check that the host name is correct." % self.ftpServerLabel.text())
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
                self.statusLabel.setText("Canceled download of %s." % self.outFile.fileName())
                self.outFile.close()
                self.outFile.remove()
            else:
                self.statusLabel.setText("Downloaded %s to current directory." % self.outFile.fileName())
                self.outFile.close()

            self.outFile = None
            self.enableDownloadButton()
            self.progressDialog.hide()
        elif self.ftp.currentCommand() == QtNetwork.QFtp.List:
            if not self.isDirectory:
                self.fileList.addTopLevelItem(QtGui.QTreeWidgetItem(["<empty>"]))
                self.fileList.setEnabled(False)

    def addToList(self, urlInfo):
        item = QtGui.QTreeWidgetItem()
        item.setText(0, urlInfo.name())
        item.setText(1, str(urlInfo.size()))
        item.setText(2, urlInfo.owner())
        item.setText(3, urlInfo.group())
        item.setText(4, urlInfo.lastModified().toString('MMM dd yyyy'))

        if urlInfo.isDir():
            icon = QtGui.QIcon(':/images/dir.png')
        else:
            icon = QtGui.QIcon(':/images/file.png')
        item.setIcon(0, icon)

        self.isDirectory[urlInfo.name()] = urlInfo.isDir()
        self.fileList.addTopLevelItem(item)
        if not self.fileList.currentItem():
            self.fileList.setCurrentItem(self.fileList.topLevelItem(0))
            self.fileList.setEnabled(True)

    def processItem(self, item):
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
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()

        dirs = self.currentPath.split('/')
        if len(dirs) == 2:
            self.currentPath = '/'
            self.ftp.cd(self.currentPath)
            self.cdToParentButton.setEnabled(False)
        else :
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp.cd(self.currentPath)

        self.ftp.list()
    
    def change_path(self,path):
        self.ftp = QtNetwork.QFtp(self)
        self.setCursor(QtCore.Qt.WaitCursor)
        self.fileList.clear()
        self.isDirectory.clear()
        self.ftp.cd(path)
        self.ftp.list()

    def updateDataTransferProgress(self, readBytes, totalBytes):
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(readBytes)

    def enableDownloadButton(self):
        current = self.fileList.currentItem()
        if current:
            currentFile = current.text(0)
            self.downloadButton.setEnabled(not self.isDirectory.get(currentFile))
        else:
            self.downloadButton.setEnabled(False)

    def mongo_connector(self):
        # Connect to mongoDB and return a connection object.
        try:
            c = MongoClient(host="localhost", port=27017)
        except ConnectionFailure, error:
            sys.stderr.write("Could not connect to MongoDB: {}".format(error))
        else:
            print "Connected successfully"

        return c[self.dbname]

    def search(self):
        MESSAGE = QtCore.QT_TR_NOOP("<p>You have an erron in your connection.</p>"
                                "<p>Please select one of the server names and connect to it.</p>")
        text,ok=self.dialogbox.getText(QtGui.QInputDialog(),"Search for file",'Enter the name of your file ',QtGui.QLineEdit.Normal)
        if ok:
            try:
                total_find = {}
                regex = self.cal_regex(text)
                for servername in self.selected_SERVER_NAMES:
                    results = self.mongo_cursor[servername].find(
                        {"$or":[{"path":{"$regex":regex}},{"files":{'$regex':regex}}]})  
                    paths = [i['path'] for i in results]
                    total_find[servername] = paths
                match_path_number = sum(map(len,total_find.values()))
                if match_path_number:
                    self.wid = Path_results(self.SERVER_NAMES, total_find, match_path_number)
                    self.wid.resize(350, 650)
                    self.wid.setWindowTitle('NewWindow')
                    self.wid.show()
                else:
                    MESSAGE="""<p>No results.<p>Please try with another pattern.</p>"""
                    QtGui.QMessageBox.information(self,"QMessageBox.information()", MESSAGE)

            except IOError:
                MESSAGE="""<p>Unfortunately there is no collections with the name of this server in database.
                </p>Press OK to regural search.<p>It may takes between 2 to 10 minute.</p>"""
                QtGui.QMessageBox.information(self,
                "QMessageBox.information()", MESSAGE)
                #self.fileList.clear()
                #self.isDirectory.clear()
                #self.setCursor(QtCore.Qt.WaitCursor)
                #self.regural_search(text,self.servername,self.ftpServerLabel.text())
    
    def cal_regex(self, text):
        synonyms = wordnet.synsets(text)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        print lemmas
        pre_regex = '|'.join(lemmas)
        return re.compile(r'.*{}.*'.format(pre_regex),re.I)

    def regural_search(self, word, ftp, severname, sever_url):
        try:
            FT=ftp_walker(j)
            FT.run(word)
        except ftplib.error_temp as e:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", e)
        except ftplib.error_perm as e:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", e)
        except socket.gaierror as e:
            QtGui.QMessageBox.information(self,"QMessageBox.information()", e)
        else:
            paths = FT.all_path
            if paths:
                self.wid = Path_results(ftp, paths, servername)
                self.wid.resize(350, 650)
                self.wid.setWindowTitle('NewWindow')
                self.wid.show()
            else:
                MESSAGE="""<p>No results.<p>Please try with another pattern.</p>"""
                QtGui.QMessageBox.information(self,"QMessageBox.information()", MESSAGE)

    def add_server_for_search(self):
        self.Select_s.resize(350, 650)
        self.Select_s.setWindowTitle('Select server')
        self.Select_s.show()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ftpWin_ = FtpWindow()
    COLLECTION_NAMES = ftpWin_.collection_names
    selected_s = SelectServers
    ftpWin = FtpWindow(selected_s)
    COLLECTION_NAMES = ftpWin.collection_names
    ftpWin.show()
    sys.exit(ftpWin.exec_())
