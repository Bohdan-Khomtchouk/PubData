# cimport cython


cdef float weight(self, str S, str W):
    cdef int word_factor = max(0, 1 - self.counter[W] / self.sum5)
    cdef float other_words_factor = sum(max(0, 1 - self.counter[w] / self.sum5) for w in self.main_dict[S])
    return word_factor / other_words_factor


cdef float affinity_WS(self, str W, str S):
    return self.latest_WSM[W][self.word_with_indices[S]].max()


cdef float affinity_SW(self, str S, str W):
    return self.latest_SSM[S][self.sentence_with_indices[W]].max()


cdef float similarity_W_c(self, str W1, str W2):
    return sum(weight(self, s, W1) * affinity_SW(self, s, W2)
               for s in self.s_include_word[W1])

cdef float similarity_S_c(self, str S1, str S2):
    return sum(weight(self, S1, w) * affinity_WS(self, w, S2)
               for w in self.main_dict[S1])


def similarity_W(self, str W1, str W2):
    return similarity_W_c(self, W1, W2)


def similarity_S(self, str S1, str S2):
    return similarity_S_c(self, S1, S2)
