#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import json
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from string import punctuation
import codecs
import re


bio_words = {'cell', 'species', 'blood', 'body', 'group', 'plant', 'water', 'system', 'protein', 'membrane',
             'acid', 'organism', 'structure', 'growth', 'tion', 'molecule', 'chromosome', 'food', 'disease',
             'gene', 'tissue', 'medicine', 'amino', 'population', 'atom', 'animals', 'reaction', 'enzyme',
             'carbon', 'physiology', 'heart', 'substance', 'nerve', 'bacteria', 'electron', 'hydrogen',
             'hormone', 'muscle', 'compound', 'skin', 'embryo', 'oxygen', 'synthesis', 'result', 'immune',
             'brain', 'insect', 'human', 'ion', 'bond', 'chemistry', 'gland', 'bone', 'iron', 'oxidation',
             'family', 'source', 'complex', 'concentration', 'entity', 'united', 'mammal', 'human', 'south',
             'parent', 'pairs', 'mRNA', 'chemical', 'birds', 'organ', 'environment', 'charge', 'sequence',
             'cavity', 'reaction', 'vessel', 'earth', 'radiation', 'leaf', 'sperm', 'dioxide', 'eggs', 'nuclei',
             'flower', 'nutrients', 'head', 'drug', 'lungs', 'absorption', 'metal', 'fluid', 'phosphate', 'strand',
             'plasma', 'root', 'movement', 'metabolism', 'copper', 'adult', 'calcium', 'respiratory', 'algae',
             'kidney', 'receptor', 'fungi', 'stimulus', 'tree', 'nitrogen', 'soil', 'stem', 'sugar', 'father',
             'cytoplasm', 'neuron', 'pattern', 'copy', 'evolution', 'reptil', 'gametes', 'transfer', 'ACID',
             'sensory', 'spore', 'salt', 'fiber', 'pollen', 'tract', 'cleavage', 'allele', 'rain', 'marine',
             'fatty', 'weight', 'mutation', 'light', 'filament', 'disorder', 'habitat', 'signal', 'virus'}


def refiner(words):
    words = [w.strip(punctuation) for w in words if w not in {'e.g.', 'i.e.'}]
    wnl = WordNetLemmatizer()
    return [w[0].lower() + w[1:] if w.capitalize() == w else w for w in [wnl.lemmatize(w) for w in words]]


bio_words = refiner(bio_words)

with codecs.open('corpus.json', encoding="UTF-8") as f:
    crp = json.load(f)

with open('englishwords.txt') as f:
    words = map(str.strip, f)

    new = {}
    for key, value in crp.items():
        try:
            key = re.sub(r'[^\s\w/().-]|\(.\)', '', re.sub(u'\u2013', '-', key), re.U)
        finally:
            try:
                m = re.search(r'([^()]+)(?:\(([^)]+)\))?(.*)', key)
                k, opt, rest = m.groups()
            except Exception as exp:
                print(exp)
            else:
                refined = set(refiner(value))
                preserved = refined.intersection(bio_words)
                value = list(refined.difference(words).union(preserved))
                if opt:
                    opt = opt.replace('syn.', '')
                    if '(' in rest:
                        rest = ' '.join(re.findall(r'\(([^)]+)\)', rest))
                    new[k + ' ' + rest] = value
                    new[opt + ' ' + rest] = value
                else:
                    new[k] = value

with codecs.open('corpus_new.json', 'w', encoding='UTF-8') as f:
    refined = {k: [i.lower() for i, tag in pos_tag(v) if tag == 'NN'] for k, v in new.items()}
    json.dump(refined, f, indent=4)
