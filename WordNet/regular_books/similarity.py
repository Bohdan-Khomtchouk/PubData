import numpy as np
from itertools import chain
from functools import wraps
import json
import glob


class Initializer:
    def __init__(self, *args):
        self.main_dict = self.load_data()
        self.all_words = self.create_words()
        self.all_sent = self.get_sentences()

    def load_data(self):
        file_names = glob.glob("*.json")
        result = {}
        for name in file_names:
            with open(name) as f:
                result.update(json.load(f))
        return result

    def create_words(self):
        all_words = set().union(*chain.from_iterable(self.main_dict.values()))
        return list(all_words)

    def get_sentences(self):
        return list(map(str, self.main_dict))

    def create_WSM(self, all_words):
        """
        Initialize the word similarity matrix by creating a matrix with
        1 as its main digonal and columns with word names.
        """
        dt = np.dtype({"names": all_words, "formats": ['f4'] * len(all_words)})
        wsm = np.zeros(len(all_words), dtype=dt)
        wsm_view = wsm.view('f4').reshape(len(all_words), -1)
        np.fill_diagonal(wsm_view, 1)
        return wsm

    def create_SSM(self):
        """
        Initialize the sentence similarity matrix by creating a NxN zero filled
        matrix where N is the number of sentences.
        """
        size = len(self.main_dict)
        dt = np.dtype({"names": self.all_sent,
                       "formats": ['f4'] * size})
        return np.zeros(size, dtype=dt)


class FindSimilarity(Initializer):
    def __init__(self, *args):
        super(FindSimilarity, self).__init__(*args)
        self.latest_WSM = self.create_WSM()
        self.latest_SSM = self.create_SSM()

    def cache_matrix(self, f):
        cache_WSM = {}
        cache_SSM = {}
        if f.__name__ == "WSM":
            cache = cache_WSM
        else:
            cache = cache_SSM

        @wraps(f)
        def wrapped(n):
            try:
                result = cache[n]
            except KeyError:
                result = cache[n] = f(n)
            return result
        return wrapped

    def affinity_WS(self, W, S, n):
        max(self.WSM(W, wi, n) for wi in self.main_dict[S])

    def affinity_SW(self, S, W, n):
        max(self.SSM(S, sj, n) for sj in self.sentence_include_word(W))

    def similarity_W(self, W1, W2, n):
        sum(self.weight(s, W1) * self.affinity_WS(s, W2, n - 1)
            for s in self.sentence_include_word(W1))

    def similarity_S(self, S1, S2, n):
        sum(self.weight(w, S1) * self.affinity_WS(w, S2, n - 1) for w in self.main_dict[S1])

    def sentence_include_word(self, word):
        return {str(sent) for sent, words in self.main_dict.items() if word in words}

    def update_WSM(self):
        for w in self.all_words:
            for index in range(len(self.all_words)):
                self.latest_WSM[w][index] = self.similarity_W(w, self.all_words[index])

    def update_SSM(self):
        for s in self.all_sent:
            for index in range(len(self.all_sent)):
                self.latest_SSM[s][index] = self.similarity_S(s, self.all_sent[index])

    @cache_matrix
    def WSM(self, n):
        if n > 0:
            self.update_WSM()
        return self.latest_WSM

    @cache_matrix
    def SSM(self, n):
        if n > 0:
            self.update_SSM()
        return self.latest_SSM

    def weight(self):
        pass
