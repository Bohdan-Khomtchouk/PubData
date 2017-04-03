


import re
from importlib import reload
from os import path as ospath
from sys import argv, exit, path as syspath
from itertools import chain
from collections import OrderedDict
from interface.extras.extras import general_style
from PyQt4.QtCore import pyqtSlot, SIGNAL
from PyQt4 import QtCore, QtGui, QtNetwork
from nltk.corpus import wordnet
from .searchpath.searchpath import Path_results
from .editserver.editserver import Edit_servers
from .selectservers.selectservers import SelectServers
import sqlite3 as lite
from .updateservers.updateservers import Update
from ast import literal_eval
from string import punctuation
syspath.append(ospath.dirname(ospath.dirname(ospath.abspath(__file__))))
from recommender import recomdialog
from queue import Queue


class ftpWindow(QtGui.QWidget):
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
        self.server_items = iter(self.server_dict.items())
        self.isDirectory = {}
        self.ftp = None
        self.outFile = None
        frame_style = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.queue = Queue()
        self.thread = Update(self.queue)
        self.resume = False
        self.updating = False

        self.select_s = SelectServers(self.server_names)
        self.select_s.ok_button.clicked.connect(self.put_get_servers)
        self.select_u = SelectServers(self.server_names)
        self.select_u.ok_button.clicked.connect(self.run_namual_update)
        self.dialog = recomdialog.Searchdialog()
        self.dialog.ok_button.clicked.connect(self.get_keyword)

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
        self.cdToParentButton.setIcon(QtGui.QIcon('images/cdtoparent.png'))
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
        self.connect(self.thread, SIGNAL("update_message"), self.update_message)
        self.connect(self.thread, SIGNAL("update_again"), self.update_servers_all)

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
        icon = QtGui.QIcon("images/pubdata.png")
        self.setWindowIcon(icon)
        self.tray_icon = QtGui.QSystemTrayIcon()
        self.tray_icon.setIcon(QtGui.QIcon(icon))
        self.tray_icon.activated.connect(self.tray_click)
        self.setWindowIcon(QtGui.QIcon(icon))

    def tray_click(self, reason):
        if reason == self.tray_icon.Trigger:
            self.show()

    def closeEvent(self, event):
        if self.resume or self.updating:
            event.ignore()
            self.hide()
            self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.Tool)
            self.tray_icon.show()
            self.tray_icon.showMessage("PubData", "Updating...")

        else:
            print("EXIT!!!!")
            super(ftpWindow, self).closeEvent(event)

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

    def getServerNames(self):
        """
        .. py:attribute:: getServerNames()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        conn = lite.connect('PubData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servernames")
        d = OrderedDict([(k, v) for _, k, v in cursor.fetchall()])
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
                                              list(self.server_names),
                                              0,
                                              False)
        if ok and item:
            self.ftpServerLabel.setText(self.server_dict[item])
            self.servername = item

    def update_message(self, mtype, message):
        if mtype == 'question':
            replay = QtGui.QMessageBox.question(self,
                                                'info',
                                                message,
                                                QtGui.QMessageBox.Yes,
                                                QtGui.QMessageBox.No)
            if replay == QtGui.QMessageBox.Yes:
                self.queue.put('yes')
                self.resume = True
            else:
                self.queue.put('no')
        elif mtype == 'error':
            QtGui.QMessageBox.information(self, 'information', message)

    def update_servers_all(self):
        '''
        .. py:attribute:: update_servers_all()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        '''
        if self.thread.exiting:
            self.update_message(self, 'error', "You've already started an update!")
        try:
            self.updating = True
            name, url = next(self.server_items)
            self.statusLabel.setText("Start updating {}...".format(name))
            self.thread.render(name, url)
        except StopIteration:
            self.statusLabel.setText("Update gets finished!")

    @pyqtSlot(QtGui.QTreeWidget)
    def run_namual_update(self):
        selected_server_names = self.select_u.selected_server_names
        self.statusLabel.setText("Start manual updating ...")
        for name in selected_server_names:
            self.thread.render(name, self.server_dict[name])

    def update_servers_manual(self):
        self.updating = True
        self.select_u.resize(350, 650)
        self.select_u.setWindowTitle('Select server names to update')
        self.select_u.show()

    def editservers(self):
        """
        .. py:attribute:: editservers()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.wid = Edit_servers(self.server_dict, "PubData.db")
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
                    user_name = bytes(user_name, encoding='utf-8')
                except:
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

        print(self.fileList.currentItem().text(0))
        self.ftp.get(self.fileList.currentItem().text(0), self.outFile)

        self.progressDialog.setLabelText("Downloading %s..." % file_name)
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
            self.downloadButton.setEnabled(True)

    @pyqtSlot(QtGui.QTreeWidget)
    def put_get_servers(self):
        self.selected_names = self.select_s.selected_server_names
        self.show_dialog()

    def manual_search(self):
        self.select_s.resize(350, 650)
        self.select_s.setWindowTitle('Select server names to search')
        self.select_s.show()

    def search_all(self):
        self.statusLabel.setText("Search in servers...")
        self.show_dialog(search_all=True)

    @pyqtSlot(QtGui.QLineEdit)
    def get_keyword(self):
        keyword = self.dialog.get_keyword()
        try:
            conn = lite.connect('PubData.db')
            cursor = conn.cursor()
        except Exception as exp:
            print(exp)
            QtGui.QMessageBox.information(self, "QMessageBox.information()", str(exp))
        else:
            if self.dialog.search_all:
                self.search(self.server_names, keyword, cursor)
            else:
                self.search(self.selected_names, keyword, cursor)
            reload(recomdialog)
            self.dialog = recomdialog.Searchdialog(self.dialog.search_all)
            self.dialog.ok_button.clicked.connect(self.get_keyword)

    def show_dialog(self, search_all=False):
        self.dialog.search_all = search_all
        self.dialog.resize(350, 650)
        self.dialog.setWindowTitle('Search for keyword')
        self.dialog.show()

    def search(self, server_names, keyword, cursor):
        """
        .. py:attribute:: search()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        def run_query(word, words, t_name):
            pattern = ' OR '.join(['"*{}*"'.format(i) for i in words])
            query = u"""SELECT file_path FROM {} WHERE {} MATCH '{}';"""
            related_query = query.format(t_name, t_name, pattern.strip())
            try:
                cursor.execute(related_query)
            except:
                related = set()
            else:
                related = set(next(zip(*cursor), []))
            try:
                cursor.execute(query.format(t_name, t_name, word))
            except:
                return set(), related
            else:
                exact = set(next(zip(*cursor), []))
                return exact, related

        message = QtCore.QT_TR_NOOP(
            "<p>You have an error in your connection.</p>"
            "<p>Please select one of the server names and connect to it.</p>")

        self.statusLabel.setText("Search into selected databases. Please wait...")
        words = self.get_lemmas(keyword)
        total_find = {}
        match_path_number = 0
        self.dialog.setCursor(QtCore.Qt.WaitCursor)
        for servername in server_names:
                t_name = '_'.join(map(str.lower, servername.split()))
                try:
                    exact, related = run_query(keyword, words, t_name)
                except Exception as exp:
                    print(exp)
                    message = "There is a problem in running the queries."
                    QtGui.QMessageBox.information(self, "QMessageBox.information()", message)
                    break
                else:
                    total_find[servername] = exact, related
                    match_path_number += len(exact.union(related))
        if any(i for i in total_find.values()):
            self.dialog.setCursor(QtCore.Qt.ArrowCursor)
            self.set_recommender(keyword, *words)
            self.wid = Path_results(self.server_dict, total_find, match_path_number)
            self.wid.resize(350, 650)
            self.wid.setWindowTitle('Search')
            self.wid.show()
        else:
            self.dialog.setCursor(QtCore.Qt.ArrowCursor)
            message = """<p>No results.<p>Please try with another pattern.</p>"""
            QtGui.QMessageBox.information(self, "QMessageBox.information()", message)

    def get_lemmas(self, word):
        """
        .. py:attribute:: cal_regex()
           :param word:
           :type word:
            :rtype: UNKNOWN
        .. note::
        """
        punc = set(punctuation)
        if punc.intersection(word):
            all_words = [word] + [i for i in re.split(r'\W', word) if len(i) > 2]
            lemmas = set().union(*map(self.get_wordnet_words, all_words))
        else:
            lemmas = self.get_wordnet_words(word)
        if not len(lemmas):
            synonyms = wordnet.synsets(word.lower())
            lemmas = set(chain.from_iterable([w.lemma_names() for w in synonyms]))
            lemmas = self.get_wordnet_words(word).union(lemmas)
        return list(lemmas)

    def set_recommender(self, word, *syns):
        conn = lite.connect('PubData.db')
        cursor = conn.cursor()
        insert_query = u"""INSERT OR IGNORE INTO {} (word, rank) VALUES(?, ?);"""
        update_query = u"""UPDATE '{}' SET rank=rank+1 WHERE word='{}';"""
        try:
            cursor.execute(insert_query.format('recommender_exact'), (word, 0))
            cursor.execute(update_query.format('recommender_exact', word))
        except Exception as exp:
            print(exp)
            QtGui.QMessageBox.information(self, "QMessageBox.information()", str(exp))
        for syn in syns:
            try:
                cursor.execute(insert_query.format('recommender_syns'), (syn, 0))
                cursor.execute(update_query.format('recommender_syns', syn))
            except Exception as exp:
                print(exp)
                QtGui.QMessageBox.information(self, "QMessageBox.information()", str(exp))
        conn.commit()

    def get_wordnet_words(self, text):
        conn = lite.connect('PubData.db')
        cursor = conn.cursor()
        # remove OR synonyms LIKE '%{}%' from query
        cursor.execute("SELECT * FROM wordnet WHERE word LIKE '%{}%' COLLATE NOCASE;".format(text, text))
        seen = set()
        try:
            for _, w, syns in cursor.fetchall():
                seen |= set(literal_eval(syns)) | {w}
        except Exception as exp:
            print ('Exception: ', str(exp))
            return set()
        else:
            return set(i for i in seen if ' ' not in i)

    def add_server_for_search(self):
        """
        .. py:attribute:: add_server_for_search()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        self.Select_s.resize(350, 650)
        self.Select_s.setWindowTitle('Select server to search')
        self.Select_s.show()


def run():
    app = QtGui.QApplication(argv)
    ftpWin = ftpWindow()
    ftpWin.resize(950, 600)
    ftpWin.show()
    exit(app.exec_())
