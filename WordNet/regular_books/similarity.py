import numpy as np
from itertools import chain
from functools import wraps  # lru_cache
from collections import Counter
from itertools import combinations, tee  # permutations
from os import path as ospath
from operator import itemgetter
import json
import glob
from general import similarity_S, similarity_W
from datetime import datetime
from sys import intern


class Initializer:
    def __init__(self, *args, **kwargs):
        self.main_dict = {intern(i): set(j) for i, j in kwargs['main_dict'].items() if j}
        self.all_words = self.create_words()
        self.all_sent = self.get_sentences()

    def create_words(self):
        all_words = np.unique(np.fromiter(chain.from_iterable(self.main_dict.values()),
                              dtype='U20'))
        return all_words

    def get_sentences(self):
        return np.array(list(self.main_dict))

    def create_SSM(self):
        """
        Initialize the sentence similarity matrix by creating a NxN zero filled
        matrix where N is the number of sentences.
        """
        size = self.all_sent.size
        dt = np.dtype({"names": self.all_sent,
                       "formats": [np.float16] * size})
        return np.zeros(size, dtype=dt)


class FindSimilarity(Initializer):
    def __new__(cls, *args, **kwargs):
        """
        Defining the cache functions in __new__ method to be refreshed
        after each instantiation.
        """
        '''
        def cache_matrix(f):
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

        def cache_weight(f):
            cache = {}

            @wraps(f)
            def wrapped(**kwargs):
                key = tuple(kwargs.values())
                try:
                    result = cache[key]
                except KeyError:
                    result = cache[key] = f(**kwargs)
                return result
            return wrapped
        '''
        def cache_general(f):
            cache = {}

            @wraps(f)
            def wrapped(*args):
                try:
                    result = cache[args]
                except KeyError:
                    result = cache[args] = f(*args)
                return result
            return wrapped

        obj = object.__new__(cls)
        general_attrs = (#"affinity_WS",
                         #"affinity_SW",
                         "similarity_W",
                         "similarity_S",)
        for name in general_attrs:
            setattr(obj, name, cache_general(getattr(obj, name)))
        # setattr(obj, "weight", cache_weight(getattr(obj, "weight")))
        cache_general.cache = {}
        # cache_matrix.cache = {}
        # cache_weight.cache = {}
        return obj

    def __init__(self, *args, **kwargs):
        super(FindSimilarity, self).__init__(*args, **kwargs)
        try:
            self.iteration_number = args[0]
        except IndexError:
            raise Exception("Please provide an iteration number!")
        self.name = ospath.basename(kwargs["name"]).split('.')[0]
        # Word and the indices of its sentences.
        self.s_include_word = {w: self.sentence_include_word(w) for w in self.all_words}
        self.sentence_with_indices = self.create_sentence_with_indices()
        # Sentences and the indices of their words
        self.word_with_indices = self.create_words_with_indices()
        self.latest_WSM = self.create_WSM()
        self.latest_SSM = self.create_SSM()
        self.counter = Counter(self.all_words)
        self.sum5 = sum(j for _, j in self.counter.most_common(5)) 
        print("Finish initialization...!")

    def create_words_with_indices(self):
        w_w_i = {w: i for i, w in enumerate(self.all_words)}
        total = {}
        for s, words in self.main_dict.items():
            if len(words) > 1:
                total[s] = list(itemgetter(*words)(w_w_i))
            elif words:
                total[s] = w_w_i[next(iter(words))]
        return total

    def create_sentence_with_indices(self):
        s_w_i = {s: i for i, s in enumerate(self.all_sent)}
        total = {}
        for w in self.all_words:
            sentences = self.s_include_word[w]
            if len(sentences) > 1:
                total[w] = list(itemgetter(*sentences)(s_w_i))
            elif sentences:
                total[w] = [s_w_i[sentences.pop()]]
        return total

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

    def affinity_WS(self, W, S):
        # return max(self.WSM(n)[W][self.w_w_i[w]] for w in self.main_dict[S])
        return self.latest_WSM[W][self.word_with_indices[S]].max()

    def affinity_SW(self, S, W):
        return self.latest_SSM[S][self.sentence_with_indices[W]].max()

    def similarity_W(self, W1, W2, i):
        return similarity_W(self, W1, W2)
        # return sum(self.weight(s=s, w=W1) * self.affinity_SW(s, W2)
        #           for s in self.s_include_word[W1])

    def similarity_S(self, S1, S2, i):
        return similarity_S(self, S1, S2)
        # return sum(self.weight(w=w, s=S1) * self.affinity_WS(w, S2) for w in self.main_dict[S1])

    def sentence_include_word(self, word):
        return {sent for sent, words in self.main_dict.items() if word in words}

    def weight(self, **kwargs):
        W, S = kwargs['w'], kwargs['s']
        word_factor = max(0, 1 - self.counter[W] / self.sum5)
        other_words_factor = sum(max(0, 1 - self.counter[w] / self.sum5) for w in self.main_dict[S])
        return word_factor / other_words_factor

    def iteration(self):
        sent_comb = combinations(map(str, self.all_sent), 2)
        word_comb = combinations(map(str, self.all_words), 2)
        sent_comb = iter(tee(sent_comb, 4))
        word_comb = iter(tee(word_comb, 4))
        w_size = self.all_words.size
        s_size = self.all_sent.size
        ind_lower_s = np.tril_indices(s_size, -1)
        ind_uper_s = np.triu_indices(s_size, 1)
        ind_lower_w = np.tril_indices(w_size, -1)
        ind_uper_w = np.triu_indices(w_size, 1)
        latest_SSM_view = self.latest_SSM.view(np.float16).reshape(s_size, -1)
        latest_WSM_view = self.latest_WSM.view(np.float16).reshape(w_size, -1)
        for i in range(self.iteration_number):
            # Update SSM
            new_arr = np.array([self.similarity_S(s1, s2, i) for s1, s2 in next(sent_comb)])
            latest_SSM_view[ind_uper_s] = new_arr
            latest_SSM_view[ind_lower_s] = new_arr
            print("Finished similarity_S, iteration {}".format(i + 1))
            # Update WSM
            new_arr = np.array([self.similarity_W(w1, w2, i) for w1, w2 in next(word_comb)])
            latest_WSM_view[ind_uper_w] = new_arr
            latest_WSM_view[ind_lower_w] = new_arr
            print("Finished similarity_W, iteration {}".format(i + 1))

        self.save_matrixs()

    def save_matrixs(self):
        np.save("SSM_{}.txt".format(self.name),
                self.latest_SSM)
        np.save("WSM_{}.txt".format(self.name),
                self.latest_WSM)


if __name__ == "__main__":
    def load_data():
        file_names = glob.glob("files/*.json")
        for name in file_names:
            with open(name) as f:
                print(name)
                yield name, json.load(f)

    ld = load_data()
    next(ld)
    t = datetime.now()
    for name, d in ld:
        d = dict(list(d.items())[:400])
        FS = FindSimilarity(4, main_dict=d, name=name)
        print("All words {}".format(len(FS.all_words))),
        FS.iteration()
    print("******************")
    print("* {} *".format(datetime.now() - t))
    print("******************")
