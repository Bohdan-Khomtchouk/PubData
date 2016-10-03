# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------


from nltk import word_tokenize, sent_tokenize, pos_tag
from string import punctuation
import json

file_name = "introduction-to-computational-genomics-a-case-studies-approach.txt"
with open(file_name) as f:
    result = {hash(sent): word_tokenize(sent) for sent in sent_tokenize(f.read())}


total = {}
for k, v in result.items():
    if len(v) > 1:
        value = {w.strip(punctuation).lower() for w, tag in pos_tag(v) if 'NN' in tag and len(w) > 2}
        if value:
            total[k] = list(value)


with open("{}.json".format(file_name.split('.')[0]), 'w') as f:
    json.dump(total, f, indent=4)
