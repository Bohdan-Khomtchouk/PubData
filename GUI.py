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


from PySide import QtCore, QtGui, QtNetwork
import csv,json
import ftp_rc
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
global server_names
server_names={'Ensembl Genome Browser':'ftp.ensembl.org',
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
        with open('Server_names.json')as f:
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
        okButton.clicked.connect(self.addnew)
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
                with open('Server_names.json','w') as f:
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
                with open('Server_names.json','w') as f:
                    json.dump(self.servers,f,indent=4)

class FileInfo(QtGui.QWidget):
    def __init__(self, fileInfo, parent=None):
        super(FileInfo, self).__init__(parent)

        fileNameLabel = QtGui.QLabel("File Name:")
        fileNameEdit = QtGui.QLineEdit(fileInfo.fileName())

        pathLabel = QtGui.QLabel("Path:")
        pathValueLabel = QtGui.QLabel(fileInfo.absoluteFilePath())
        pathValueLabel.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)


        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(fileNameLabel)
        mainLayout.addWidget(fileNameEdit)
        mainLayout.addWidget(pathLabel)
        mainLayout.addWidget(pathValueLabel)
        mainLayout.addStretch(1)
        self.setLayout(mainLayout)

class Path_results(QtGui.QDialog):    
    def __init__(self,pathes,parent=None):
        super(Edit_servers, self).__init__(parent)                
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.pathes=pathes
        self.hLayout = QtGui.QHBoxLayout()
        self.mainLayout.insertLayout(0, self.hLayout)

        self.listA=QtGui.QTreeWidget()
        self.listA.setHeaderLabels(['Found Pathes'])
        self.dialogbox=QtGui.QInputDialog()
        
        for i in self.pathes:    
            item=QtGui.QTreeWidgetItem()
            item.setText(0, i)
            self.listA.addTopLevelItem(item)

        self.hLayout.addWidget(self.listA)

        self.buttonGroupbox = QtGui.QGroupBox()
        self.buttonlayout = QtGui.QVBoxLayout()
        self.buttonGroupbox.setLayout(self.buttonlayout)

        getDataButton = QtGui.QPushButton('Show path')
        getDataButton.clicked.connect(self.addnew)
        self.buttonlayout.addWidget(getDataButton)

        self.mainLayout.addWidget(self.buttonGroupbox)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}
        QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}QTreeWidgetItem{background-color:white; color:black}""")

        self.listA.itemDoubleClicked.connect(self.doubleClicked_path)

    @pyqtSlot(QtGui.QTreeWidget)
    def doubleClicked_path(self,item):
        FT=FtpWindow()
        FT.setCursor(QtCore.Qt.WaitCursor)
        FT.fileList.clear()
        FT.isDirectory.clear()
        FT.ftp.cd(item.text(0))
        FT.ftp.list()

class FtpWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        super(FtpWindow, self).__init__(parent)
        self.defaulturl='ftp://ftp.xenbase.org/pub/Genomics/Sequences'
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
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

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialogbox=QtGui.QInputDialog()

        self.quitButton = QtGui.QPushButton("Quit")
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.dialogbox=QtGui.QInputDialog()
        
        self.EditserverButton = QtGui.QPushButton("Editservers")
        
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        buttonBox.addButton(self.EditserverButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.downloadButton,QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
        buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)

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
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}QInputDialog {border-radius:4px;color :black;font-weight:500; font-size: 12pt}""")

    def select(self):
        global servers

        try:
            with open('Server_names.json')as f:
                servers=json.load(f)

                item, ok = QtGui.QInputDialog.getItem(self, "Select the server name ",
                        "Season:", servers.keys(), 0, False)
                if ok and item:
                    self.ftpServerLabel.setText(servers[item])
        
        except IOError:
            print("Can't find server file.")
            with open('Server_names.json','w')as f:
                json.dump(server_names,f,indent=4)
            print("Server names has beed rewrite, you can try again.")

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
        if len(dirs) > 1:
            self.currentPath = ''
            self.cdToParentButton.setEnabled(False)
            self.ftp.cd('/')
        else:
            self.currentPath = '/'.join(dirs[:-1])
            self.ftp.cd(self.currentPath)

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

    def search(self):
        MESSAGE = QtCore.QT_TR_NOOP("<p>You have an erron in your connection.</p>"
                                "<p>Please select one of the server names and connect to it.</p>")
        text,ok=self.dialogbox.getText(QtGui.QInputDialog(),"Search for file",'Enter the name of your file ',QtGui.QLineEdit.Normal)
        if ok:
            try :
                self.outFile = QtCore.QFile('biocsv.csv')
                self.filename = 'BioNetHub.csv'
                try:
                    self.ftp.get(text,self.outFile)
                except AttributeError:
                    QtGui.QMessageBox.critical(self, self.tr("QMessageBox.showCritical()"),
                                               MESSAGE, 1|
                                               QtGui.QMessageBox.StandardButton.Ok)
                with open('BioNetHub.csv') as csvfile:
                    seen_pathes=set()
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        if any(self.name in i for i in row[1:]):
                            path= row[0]
                            seen_pathes.add(path)
                            self.setCursor(QtCore.Qt.WaitCursor)
                            self.fileList.clear()
                            self.isDirectory.clear()
                            self.ftp.cd(path)
                            self.ftp.list()
            except IOError:
                MESSAGE="Unfortunately this server doesn't provide a CSV file fro quick search"
                reply = QtGui.QMessageBox.information(self,
                "QMessageBox.information()", MESSAGE)
                



if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    ftpWin = FtpWindow()
    ftpWin.show()
    sys.exit(ftpWin.exec_())




