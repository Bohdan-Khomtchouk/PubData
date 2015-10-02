#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Thi is a GUI version for BioNetHub command line interface, written with PySide.
# For implementing this GUI in serveral parts we used PySide Examples (https://github.com/PySide/Examples)

from PySide import QtCore, QtGui, QtNetwork
import csv
import ftp_rc

global server_names
server_names={'1':'ftp.ensembl.org',
         '2':'hgdownload.cse.ucsc.edu',
         '3':'ftp.uniprot.org',
         '4':'ftp.flybase.net',
         '5':'ftp.xenbase.org',
         '6':'ftp.arabidopsis.org/home',
         '7':'rgd.mcw.edu',
         '8':'ftp.ncbi.nlm.nih.gov'}

class TabDialog(QtGui.QDialog):
    def __init__(self, fileName, parent=None):
        super(TabDialog, self).__init__(parent)

        fileInfo = QtCore.QFileInfo(fileName)

        tabWidget = QtGui.QTabWidget()
        tabWidget.addTab(FileInfo(fileInfo), "FileIno")
        tabWidget.addTab(ServersTab(fileInfo), "Servers")

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(tabWidget)
        self.setLayout(mainLayout)
        self.searchButton = QtGui.QPushButton("Smart Search")
        self.setWindowTitle("Tab Dialog")
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.searchButton, QtGui.QDialogButtonBox.ActionRole)
        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}""")

class ServersDialog(QtGui.QDialog):
    def __init__(self, fileName, parent=None):
        super(ServersDialog, self).__init__(parent)

        topLabel = QtGui.QLabel("Open with:")

        self.applicationsListBox = QtGui.QListWidget()
        self.applications = []

        for i,j in server_names.items():
            self.applications.append("{}.{}".format(i,j))

        self.applicationsListBox.insertItems(0, self.applications)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(topLabel)
        layout.addWidget(self.applicationsListBox)
        self.selectButton = QtGui.QPushButton('select')
        self.editButton = QtGui.QPushButton('edit')
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.selectButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.editButton,QtGui.QDialogButtonBox.ActionRole)

        self.selectButton.clicked.connect(self.select)
        self.editButton.clicked.connect(self.edit)


        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.setStyleSheet("""QWidget {border-radius:4px;color :black;font-weight:500; font-size: 12pt}
        QPushButton{color:#099ff0;border-style: outset;border-width: 2px;border-radius: 10px;
        border-color: beige;font: bold 14px;min-width: 10em;padding: 8px;}QPushButton:pressed { background-color: orange }
        QLineEdit{background-color:white; color:black}QTextEdit{background-color:#ffffff; color:#000000}""")

    def select(self):   
        items = ("Spring", "Summer", "Fall", "Winter")

        item, ok = QtGui.QInputDialog.getItem(self, "QInputDialog.getItem()",
                "Season:", items, 0, False)
        if ok and item:
            self.itemLabel.setText(item)

    def edit(self):
        print self.applicationsListBox.takeItem(2).text()
        pass


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
        
        
        buttonBox = QtGui.QDialogButtonBox()
        buttonBox.addButton(self.downloadButton,
                QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(self.quitButton, QtGui.QDialogButtonBox.RejectRole)
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

        try:
            with open('servers.txt') as f:

                servers=[i.strip() for i in f]
                item, ok = QtGui.QInputDialog.getItem(self, "QInputDialog.getItem()",
                        "Season:", servers, 0, False)
                if ok and item:
                    self.ftpServerLabel.setText(item)
        except IOError:
            with open('servers.txt','w') as f:
                for line in server_names.values():
                    f.write(line+'\n')

    def sizeHint(self):
        return QtCore.QSize(800, 400)

    def showservers(self):
        self.se = ServersDialog('server_list')
        self.se.setGeometry(100, 200, 600, 400)
        self.se.show()

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
        text,ok=self.dialogbox.getText(QtGui.QInputDialog(),"Search for file",'Enter the name of your file ',QtGui.QLineEdit.Normal)
        if ok:
            try :
                self.outFile = QtCore.QFile('biocsv.csv')
                self.filename = 'BioNetHub.csv'
                self.ftp.get(text,self.outFile)
                with open('BioNetHub.csv') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=',')
                    for row in spamreader:
                        if self.name in row:
                            path= row[0]
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

