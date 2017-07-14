import re
from importlib import reload
from os import path as ospath, makedirs
import sys
from itertools import chain
from collections import OrderedDict
from nltk.corpus import wordnet
import sqlite3 as lite
from ast import literal_eval
from string import punctuation
from queue import Queue


def search(self, server_names, keyword, cursor):
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
    words = self.get_lemmas(keyword)
    total_find = {}
    match_path_number = 0

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
        self.wid = Path_results(self.image_path, self.server_dict, total_find, match_path_number)
        self.wid.resize(350, 650)
        self.wid.setWindowTitle('Search')
        self.wid.show()
    else:
        self.dialog.setCursor(QtCore.Qt.ArrowCursor)
        message = """<p>No results.<p>Please try with another pattern.</p>"""
        QtGui.QMessageBox.information(self, "QMessageBox.information()", message)

def get_lemmas(self, word):
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
    conn = lite.connect(self.recommender_db_path)
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
    conn = lite.connect(self.db_path)
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