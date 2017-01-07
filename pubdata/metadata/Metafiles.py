#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from interface.extras.extras import general_style



class Meta(QtGui.QDialog):
    def __init__(self, root, parent=None):
        super(Meta, self).__init__(parent)
        self.current_path = os.path.join(os.path.dirname(QtCore.QDir.currentPath()),
                                         'database/all_meta',
                                         root)
        self.main_layout = QtGui.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(self.current_path)
        self.tree = QtGui.QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.current_path))
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.clicked.connect(self.on_treeView_clicked)
        self.main_layout.addWidget(self.tree)
        self.setStyleSheet(general_style)

    @pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        # fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(filePath))