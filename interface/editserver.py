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

"""
==============
``Edit_servers``
----------
Let users update the servers optionally.
"""
from extras import general_style
from PyQt4.QtCore import pyqtSlot
from PySide import QtCore, QtGui
import json


class Edit_servers(QtGui.QDialog):
    def __init__(self, servers, parent=None):
        """
        .. py:attribute:: __init__(server)
           :param server: Server names and addresses
           :type server: dict
        .. note::
        .. todo::
        """
        super(Edit_servers, self).__init__(parent)
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.h_layout = QtGui.QHBoxLayout()
        self.main_layout.insertLayout(0, self.h_layout)

        self.list_a = QtGui.QTreeWidget()
        self.list_a.setHeaderLabels(['Server names'])
        self.dialog_box = QtGui.QInputDialog()
        self.servers = servers

        for i in self.servers:
            item = QtGui.QTreeWidgetItem()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            item.setText(0, i)
            self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)

        self.button_group_box = QtGui.QGroupBox()
        self.button_layout = QtGui.QVBoxLayout()
        self.button_group_box.setLayout(self.button_layout)

        get_data_button = QtGui.QPushButton('Add new server')
        get_data_button.clicked.connect(self.addnew)
        self.button_layout.addWidget(get_data_button)

        ok_button = QtGui.QPushButton('Remove selected')
        ok_button.clicked.connect(self.removeSel)
        self.button_layout.addWidget(ok_button)

        self.main_layout.addWidget(self.button_group_box)
        self.setStyleSheet(general_style)

        self.list_a.itemDoubleClicked.connect(self.doubleClickedSlot)

    def itemadder(self, name):
        """
        Create the list of server names.
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
        Launch the relative pop-up windows for editing the names and addresses of servers,
        by double-clicking on items in the list.
        .. py:attribute:: doubleClickedSlot()
           :param item:
           :type item:
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        current_name = item.text(0)
        name, ok = self.dialog_box.getText(self,
                                           "Edit server name",
                                           "Edit the name : {}".format(current_name))
        if ok:

            address, ok = self.dialog_box.getText(self,
                                                  "Edit server address!",
                                                  "Edit the address : {}".format(self.servers[current_name]))
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
        Remove the checked items.
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
        for item in checked_items:
            item_index = self.list_a.indexOfTopLevelItem(item)
            self.list_a.takeTopLevelItem(item_index)


    def addnew(self):
        """
        Add new server.
        .. py:attribute:: addnew()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        name, ok = self.dialog_box.getText(self,
                                           "Add server name",
                                           "Add the name")
        if ok:
            address, ok = self.dialog_box.getText(self,
                                                  "Add server address",
                                                  "Add the address")
            if ok:
                self.servers[name] = address
                self.itemadder(name)
                with open('data/SERVER_NAMES.json', 'w') as f:
                    json.dump(self.servers, f, indent=4)