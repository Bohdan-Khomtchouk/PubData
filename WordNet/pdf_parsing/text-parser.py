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
Create a JSON file containing the encyclopedia words and relative descriptions. The result is not precisely the same as the PDF,
approximately 95% is correct (the desired content is correct, the rest is garbage, e.g., table of contents, appendices, misc footnotes).

"""

import json
from collections import OrderedDict
import codecs
from xml.etree import ElementTree
from itertools import chain
from operator import itemgetter



class Mainparser():
    def __init__(self, *args, **kwargs):
        self.json_file_name = kwargs['jfn']
        self.xml_file_name = kwargs['xfn']

    def read_word_json(self):
        with open(self.json_file_name) as f:
            return json.load(f)

    def pager(self):
        with open(self.xml_file_name) as f:
            tree = ElementTree.parse(f)
        root = tree.getroot()
        for neighbor in root.iter('page'):
            sub = [[node.text] if node.text else [sub.text + ' ' if sub.text else '' for sub in node.getchildren()] for node in neighbor.getchildren()]
            sub = chain.from_iterable(sub)
            if neighbor.text:
                yield (int(neighbor.get('number')) - 17, neighbor.text + ''.join(sub))

    def create_dict(self):
        return OrderedDict(self.pager())

    def new_dict(self):
        words = self.read_word_json()
        new_dict = {}
        for k, v in words.items():
            for i in v:
                new_dict.setdefault(i, []).append(k)
        return new_dict

    def combiner(self):
        text_dict = self.create_dict()
        words_dict = self.new_dict()
        new_dict = OrderedDict()
        for k, v in text_dict.items():
            new_dict.update({tuple(words_dict.get(k, '')): v})
        return new_dict

    def splitter(self):
        word_text = self.combiner()
        for words, text in word_text.items():
            pairs = sorted([(word, text.find(word)) for word in words], key=itemgetter(1)) + [('', None)]
            pairs = [(word, index) for word, index in pairs if index != -1]
            all_slices = [(word, text[index + len(word):next_ind]) for (word, index), (_, next_ind) in zip(pairs, pairs[1:])]
            yield all_slices

    def create_json(self):
        words = OrderedDict(chain.from_iterable(self.splitter()))
        # words = OrderedDict(chain(self.pager()))
        with codecs.open('pages.json', 'w', encoding='UTF-8') as f:
            json.dump(words, f, indent=4)


if __name__ == '__main__':
    MP = Mainparser(xfn='Encyclopedia_of_Biology_pages.xml',
                    jfn='words.json')

    MP.create_json()
