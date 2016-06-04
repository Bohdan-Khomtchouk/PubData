# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------
from PySide import QtGui
from extras import general_style
import sqlite3 as lite


class Searchdialog(QtGui.QDialog):
    """
    ==============
    ``Searchdialog``
    ----------
    .. py:class:: Searchdialog()
    """
    def __init__(self, search_all=False, parent=None):
        """
        .. py:attribute:: __init__()
            :rtype: UNKNOWN
        .. note::
        .. todo::
        """
        super(Searchdialog, self).__init__(parent)
        self.search_all = search_all
        self.main_layout = QtGui.QVBoxLayout()
        self.texteditor = QtGui.QTextEdit()
        self.texteditor.setReadOnly(True)
        self.texteditor.setHtml(self.get_recommended_words())
        self.lineedit = QtGui.QLineEdit()
        self.ok_button = QtGui.QPushButton('Search')
        label1 = QtGui.QLabel("Enter your keyword here:")
        label2 = QtGui.QLabel("<font color='#009933'><b>Recommended</b> words:</font>")
        self.main_layout.addWidget(label1)
        self.main_layout.addWidget(self.lineedit)
        self.main_layout.addWidget(self.ok_button)
        self.main_layout.addWidget(label2)
        self.main_layout.addWidget(self.texteditor)
        self.setLayout(self.main_layout)
        self.setStyleSheet(general_style)

    def get_keyword(self):
        return self.lineedit.text().strip()

    def get_recommended_words(self):
        conn = lite.connect('../PubData.db')
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM 'recommender_exact' ORDER BY rank DESC LIMIT 12")
        try:
            exact = zip(*cursor.fetchall())[0]
            print exact
            cursor.execute("SELECT word FROM 'recommender_syns' ORDER BY rank DESC LIMIT 20")
            syns = zip(*cursor.fetchall())[0]
        except IndexError:
            exact = syns = []
        text = """
                <ul>
                    <li><font color='red'><b>Exact words:</b></font></li>
                        <ul>
                            {}
                        </ul>
                    <li><font color='red'><b>Similar words:</b></font></li>
                        <ul>
                            {}
                        <ul>
                </ul>
               """

        return text.format('\n'.join(["<li>{}</li>".format(i) for i in exact]),
                           '\n'.join(["<li>{}</li>".format(j) for j in syns]))
