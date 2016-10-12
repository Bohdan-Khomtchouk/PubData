# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------


from nltk import word_tokenize, sent_tokenize, pos_tag
from string import punctuation
import json
import glob
import re


def refine_data(main_dict):
    regex1 = re.compile(r'[a-zA-Z]', re.U)
    regex2 = re.compile(r'[^a-zA-Z]', re.U)
    regex3 = re.compile(r'[^\w]*(\w+)[^\w]*$', re.U)

    def check_word(w):
        a = not bool({"*", "+", "/", ","}.intersection(w))
        b = len(regex1.findall(w)) > 2
        c = not(len(regex2.findall(w)) > 2)
        d = 2 < len(w) < 20
        return a and b and c and d

    result = {k: [regex3.search(w).group(1) for w in v if check_word(w)]
              for k, v in main_dict.items() if v}
    result = {k: [w for w in v if check_word(w)] for k, v in result.items() if v}
    return {str(k): v for k, v in result.items() if v}


def create_jsons():
    for file_name in glob.glob("files/*.txt"):
        with open(file_name) as f:
            result = {hash(sent): word_tokenize(sent) for sent in sent_tokenize(f.read())}

        total = {}
        for k, v in result.items():
            if len(v) > 1:
                value = {w.strip(punctuation).lower() for w, tag in pos_tag(v) if 'NN' in tag and len(w) > 2}
                if value:
                    total[k] = list(value)

    with open("{}.json".format(file_name.split('.')[0]), 'w') as f:
        json.dump(refine_data(total), f, indent=4)


create_jsons()
