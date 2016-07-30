#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------

"""
==============
``Edit_servers``
----------
Let users update the servers optionally.
"""
from PyQt4.QtCore import pyqtSlot
from PyQt4 import QtCore, QtGui
import sqlite3 as lite
from interface.extras.extras import general_style


class Edit_servers(QtGui.QDialog):
    def __init__(self, servers, db_path, parent=None):
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
        self.db_path = db_path
        self.cursor = self.cursorcreator()

        for i in self.servers:
            item = QtGui.QTreeWidgetItem()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            item.setText(0, i)
            self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)

        self.button_group_box = QtGui.QGroupBox()
        self.button_layout = QtGui.QVBoxLayout()
        self.button_group_box.setLayout(self.button_layout)

        label = QtGui.QLabel("<font color='#009933' size=2>Double click on server names for edit</font>")
        self.main_layout.addWidget(label)

        get_data_button = QtGui.QPushButton('Add new server')
        get_data_button.clicked.connect(self.addnew)
        self.button_layout.addWidget(get_data_button)

        ok_button = QtGui.QPushButton('Remove selected')
        ok_button.clicked.connect(self.removeSel)
        self.button_layout.addWidget(ok_button)

        self.main_layout.addWidget(self.button_group_box)
        self.setStyleSheet(general_style)

        self.list_a.itemDoubleClicked.connect(self.doubleClickedSlot)

    def cursorcreator(self):
        self.conn = lite.connect(self.db_path)
        return self.conn.cursor()

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
                item_index = self.list_a.indexOfTopLevelItem(item)
                self.list_a.takeTopLevelItem(item_index)
                self.itemadder(name)
                self.cursor.execute("UPDATE servernames SET name='{}', url='{}' WHERE name='{}'".format(name,
                                                                                                        address,
                                                                                                        current_name))
                self.conn.commit()


    def removeSel(self):
        """
        Remove the checked items.
        .. py:attribute:: removeSel()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        checked_items = []
        list_items = self.list_a.invisibleRootItem()
        child_count = list_items.childCount()
        if not list_items:
            return
        for i in range(child_count):
            item = list_items.child(i)
            if item.checkState(0):
                checked_items.append(item)
        for item in checked_items:
            item_index = self.list_a.indexOfTopLevelItem(item)
            self.list_a.takeTopLevelItem(item_index)
            self.cursor.execute("DELETE FROM servernames WHERE name=?", (item.text(0),))
            self.conn.commit()

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
                self.cursor.execute("INSERT INTO servernames (name, url) VALUES (?, ?)",(name, address))
                self.conn.commit()
