#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# This file is part of PubData.

# -------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
"""
Create a JSON file containing the words of Singleton P. Dictionary of DNA and genome technology and relative descriptions. The result is not precisely the same as the PDF,
approximately 95% is correct (the desired content is correct, the rest is extra, e.g., table of contents, appendices, misc footnotes).

"""

import json
from collections import OrderedDict, deque
import codecs
from lxml.etree import XMLParser
from xml.etree import ElementTree
from itertools import chain, dropwhile
from nltk import word_tokenize, pos_tag
from re import sub

class Mainparser():
    def __init__(self, *args, **kwargs):
        self.xml_file_name = kwargs['xfn']

    def pager(self):
        word_dict = OrderedDict()
        with open(self.xml_file_name) as f:
            parser = XMLParser(recover=True)
            tree = ElementTree.parse(f, parser)
        root = tree.getroot()

        def separate(neighbor):
            d = deque()
            while True:
                try:
                    item = next(neighbor)
                except StopIteration:
                    yield d
                    break
                else:
                    if item.get('height') == '10' and item.get('font') == '5':
                        if d:
                            yield d
                            d.clear()
                            d.append(item)
                        else:
                            d.append(item)
                    else:
                        d.append(item)

        for neighbor in dropwhile(lambda x: x.get('number') != '20', root.iter('page')):
            items = separate(neighbor.iter('text'))
            for item in items:
                if item:
                    first = item.popleft()
                    if first.get('height') == '10' and first.get('font') == '5':
                        if None in item:
                            word_dict[first.text] = '\n'.join([unicode(i.text) for i in item])
                        else:
                            word_dict[first.text] = '\n'.join([unicode(i.text) for i in item])
        return word_dict

    def refine_format(self):
        all_words = self.pager()
        new = {}
        for word, desc in all_words.items():
            nouns = []
            desc = desc.replace('-\n', '').replace('\n', ' ').replace('e.g.', '').replace('i.e.', '')
            word = sub(r'\u.{4}', '', word.replace('\u2013', '-'))
            if word:
                for w, tag in pos_tag(word_tokenize(desc)):
                    if 'NN' in tag and len(w) > 3:
                        nouns.append(w.strip('.'))
                new[word] = nouns
        return new

    def create_json(self):
        with codecs.open('final_result_dict.json', 'w', encoding='UTF-8') as f:
            json.dump(self.refine_format(), f, indent=4)


if __name__ == '__main__':
    MP = Mainparser(xfn='Singleton P. Dictionary of DNA and genome technology.xml',
                    jfn='words.json')

    MP.create_json()
