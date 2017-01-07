#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

from extras.extras import general_style
from PyQt4 import QtCore, QtGui


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

    def __init__(self, servers, parent=None):
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
        self.selected_server_names = []
        self.h_layout = QtGui.QHBoxLayout()
        self.main_layout.insertLayout(0, self.h_layout)
        self.server_names = servers
        self.list_a = QtGui.QTreeWidget()
        self.list_a.setHeaderLabels(['Server names', 'Exists in DB'])
        self.dialog_box = QtGui.QInputDialog()

        for i in self.server_names:
            item = QtGui.QTreeWidgetItem()
            item.setCheckState(0, QtCore.Qt.Unchecked)
            item.setText(0, i)
            item.setText(1, 'YES')
            # item.setDisabled(True)
            self.list_a.addTopLevelItem(item)

        self.h_layout.addWidget(self.list_a)

        self.button_group_box = QtGui.QGroupBox()
        self.button_layout = QtGui.QVBoxLayout()
        self.button_group_box.setLayout(self.button_layout)

        self.ok_button = QtGui.QPushButton('OK')
        self.ok_button.clicked.connect(self.get_selected_servers)
        self.button_layout.addWidget(self.ok_button)

        self.main_layout.addWidget(self.button_group_box)
        self.setStyleSheet(general_style)

    def get_selected_servers(self):
        """
        .. py:attribute:: get_selected_servers()
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
        self.selected_server_names = [i.text(0) for i in checked_items]
        self.close()
