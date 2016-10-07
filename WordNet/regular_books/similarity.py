# -*- coding: utf-8 -*-

# Copyright (C) 2015-2016 Bohdan Khomtchouk and Kasra A. Vand
# This file is part of PubData.

# -------------------------------------------------------------------------------------------

import numpy as np
from itertools import chain
from functools import wraps
from collections import Counter
from itertools import permutations
from os import path as ospath
import json
import glob
import re


class Initializer:
    def __init__(self, *args, **kwargs):
        self.main_dict = kwargs["main_dict"]
        self.all_words = self.create_words()
        self.w_w_i = self.create_words_with_indices()
        self.all_sent = self.get_sentences()
        self.s_w_i = self.create_sentences_with_indices()

    def create_words_with_indices(self):
        return {w: i for i, w in enumerate(self.all_words)}

    def create_sentences_with_indices(self):
        return {s: i for i, s in enumerate(self.all_sent)}

    def create_words(self):
        all_words = np.unique(np.fromiter(chain.from_iterable(self.main_dict.values()),
                              dtype='U20'))
        return all_words

    def get_sentences(self):
        return list(map(str, self.main_dict))

    def create_WSM(self):
        """
        Initialize the word similarity matrix by creating a matrix with
        1 as its main digonal and columns with word names.
        """
        dt = np.dtype({"names": self.all_words, "formats": [np.float16] * self.all_words.size})
        wsm = np.zeros(self.all_words.size, dtype=dt)
        wsm_view = wsm.view(np.float16).reshape(self.all_words.size, -1)
        np.fill_diagonal(wsm_view, 1)
        return wsm

    def create_SSM(self):
        """
        Initialize the sentence similarity matrix by creating a NxN zero filled
        matrix where N is the number of sentences.
        """
        size = len(self.all_sent)
        dt = np.dtype({"names": self.all_sent,
                       "formats": [np.float16] * size})
        return np.zeros(size, dtype=dt)


class FindSimilarity(Initializer):
    def __init__(self, *args, **kwargs):
        super(FindSimilarity, self).__init__(*args, **kwargs)
        try:
            self.iteration_number = args[0]
        except IndexError:
            raise Exception("Please provide an iteration number!")
        self.latest_WSM = self.create_WSM()
        self.latest_SSM = self.create_SSM()
        self.name = ospath.basename(kwargs["name"]).split('.')[0]

    def cache_matrix(f):
        cache_WSM = {}
        cache_SSM = {}
        if f.__name__ == "WSM":
            cache = cache_WSM
        else:
            cache = cache_SSM

        @wraps(f)
        def wrapped(self, *args):
            try:
                result = cache[args]
            except KeyError:
                result = cache[args] = f(self, *args)
            return result
        return wrapped

    def cache_weight(f):
        cache = {}

        @wraps(f)
        def wrapped(self, **kwargs):
            key = tuple(kwargs.values())
            try:
                result = cache[key]
            except KeyError:
                result = cache[key] = f(self, **kwargs)
            return result
        return wrapped

    def cache_general(f):
        cache = {}

        @wraps(f)
        def wrapped(self, *args):
            try:
                result = cache[args]
            except KeyError:
                result = cache[args] = f(self, *args)
            return result
        return wrapped

    @cache_general
    def affinity_WS(self, W, S, n):
        return max(self.WSM(n)[W][self.w_w_i[wi]] for wi in self.main_dict[S])

    @cache_general
    def affinity_SW(self, S, W, n):
        return max(self.SSM(n)[S][self.s_w_i[sj]] for sj in self.sentence_include_word(W))

    @cache_general
    def similarity_W(self, W1, W2, n):
        return sum(self.weight(s=s, w=W1) * self.affinity_SW(s, W2, n - 1)
                   for s in self.sentence_include_word(W1))

    @cache_general
    def similarity_S(self, S1, S2, n):
        return sum(self.weight(w=w, s=S1) * self.affinity_WS(w, S2, n - 1) for w in self.main_dict[S1])

    @cache_general
    def sentence_include_word(self, word):
        return {str(sent) for sent, words in self.main_dict.items() if word in words}

    def update_WSM(self, n):
        print("update_WSM")
        for w in self.all_words:
            for index in range(self.all_words.size):
                self.latest_WSM[w][index] = self.similarity_W(w, self.all_words[index], n)

    def update_SSM(self, n):
        print("update_SSM")
        for s in self.all_sent:
            for index in range(len(self.all_sent)):
                self.latest_SSM[s][index] = self.similarity_S(s, self.all_sent[index], n)

    @cache_matrix
    def WSM(self, n):
        if n > 0:
            self.update_WSM(n)
        return self.latest_WSM

    @cache_matrix
    def SSM(self, n):
        if n > 0:
            self.update_SSM(n)
        return self.latest_SSM

    @cache_weight
    def weight(self, **kwargs):
        W, S = kwargs['s'], kwargs['s']
        counter = Counter(self.all_words)
        sum5 = sum(j for _, j in counter.most_common(5))
        word_factor = max(0, 1 - counter[W] / sum5)
        other_words_factor = sum(max(0, 1 - counter[w] / sum5) for w in self.main_dict[S])
        return word_factor / other_words_factor

    def iteration(self):
        for i in range(1, self.iteration_number + 1):
            for s1, s2 in permutations(self.all_sent, 2):
                self.similarity_S(s1, s2, i)
            print("Finished similarity_S, iteration {}".format(i))

            for w1, w2 in permutations(self.all_words, 2):
                self.similarity_W(w1, w2, i)
            print("Finished similarity_W, iteration {}".format(i))
        self.save_matrixs()

    def save_matrixs(self):
        np.savetxt("SSM_{}.txt".format(self.name), self.latest_SSM)
        np.savetxt("WSM_{}.txt".format(self.name), self.latest_WSM)


class Loader:
    def __init__(self):
        pass

    def load_data(self):
        file_names = glob.glob("files/*.json")
        # result = {}
        for name in file_names:
            with open(name) as f:
                yield name, json.load(f)
        # return result

    def refine_data(self, main_dict):
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
                  for k, v in list(main_dict.items())[:1000] if v}
        result = {k: [w for w in v if check_word(w)] for k, v in result.items() if v}
        return {k: v for k, v in result.items() if v}

if __name__ == "__main__":
    loader = Loader()
    all_dicts = [(name, loader.refine_data(d)) for name, d in loader.load_data()]
    for name, d in all_dicts:
        FS = FindSimilarity(2, main_dict=d, name=name)
        print("All words {}".format(len(FS.all_words)))
        FS.iteration()
