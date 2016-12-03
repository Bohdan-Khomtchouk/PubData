cimport cython
from itertools import combinations, tee
import numpy as np
cimport numpy as np
from itertools import chain
from collections import Counter
from os import path as ospath
from operator import itemgetter
import json
import glob


# DTYPE = np.object
# ctypedef np.object_t DTYPE_t

cdef int iteration_number = 2
cdef dict s_include_word
cdef dict sentence_with_indices
cdef dict word_with_indices
counter = {}
cdef int sum5
cdef np.ndarray all_sent
cdef np.ndarray all_words
cdef dict main_dict
cdef np.ndarray latest_WSM
cdef np.ndarray latest_SSM


cdef tuple initial(main_dict):
    main_dict = {i: set(j) for i, j in main_dict.items() if j}
    cdef np.ndarray all_sent = np.array(list(main_dict))
    cdef np.ndarray all_words = np.unique(np.fromiter(chain.from_iterable(main_dict.values()),
                                                      dtype='U20'))
    return all_words, all_sent, main_dict

cdef dict create_words_with_indices():
    w_w_i = {w: i for i, w in enumerate(all_words)}
    total = {}
    for s, words in main_dict.items():
        if len(words) > 1:
            total[s] = list(itemgetter(*words)(w_w_i))
        elif words:
            total[s] = w_w_i[next(iter(words))]
    return total

cdef dict create_sentence_with_indices(s_include_word):
    s_w_i = {s: i for i, s in enumerate(all_sent)}
    total = {}
    for w in all_words:
        sentences = s_include_word[w]
        if len(sentences) > 1:
            total[w] = list(itemgetter(*sentences)(s_w_i))
        elif sentences:
            total[w] = [s_w_i[sentences.pop()]]
    return total

cdef set sentence_include_word(word):
    return {sent for sent, words in main_dict.items() if word in words}


cdef str name

cdef packed struct all_sent_tp:
    np.float32_t *all_sent

cdef packed struct all_words_tp:
    np.float32_t *all_words

cdef void run():
    global all_words
    global all_sent
    global s_include_word
    global sentence_with_indices
    global word_with_indices
    global counter
    global sum5
    global main_dict
    global latest_WSM
    global latest_SSM

    file_names = glob.glob("files/*.json")
    for name in file_names:
        with open(name) as f:
            print(name)
            d = json.load(f)
            d = dict(list(d.items())[:500])
        all_words, all_sent, main_dict = initial(d)
        print("All words {}".format(len(all_words)))
        latest_WSM = create_WSM()
        latest_SSM = create_SSM()
        s_include_word = {w: sentence_include_word(w) for w in all_words}
        sentence_with_indices = create_sentence_with_indices(s_include_word)
        word_with_indices = create_words_with_indices()
        counter = Counter(all_words)
        sum5 = sum(j for _, j in counter.most_common(5))
        iteration(name.split('/')[1].split('.')[0])


cdef np.ndarray create_SSM():
    """
    Initialize the sentence similarity matrix by creating a NxN zero filled
    matrix where N is the number of sentences.
    """
    cdef int size = all_sent.size
    dt = np.dtype({"names": all_sent,
                   "formats": [np.float16] * size})
    return np.zeros(size, dtype=dt)
    # return arr

cdef np.ndarray create_WSM():
    """
    Initialize the word similarity matrix by creating a matrix with
    1 as its main digonal and columns with word names.
    """
    cdef int size = all_words.size
    dt = np.dtype({"names": all_words, "formats": [np.float16] * all_words.size})
    wsm = np.zeros(size, dtype=dt)
    wsm_view = wsm.view(np.float16).reshape(size, -1)
    np.fill_diagonal(wsm_view, 1)
    return wsm


cdef float weight(str S, str W):
    cdef int word_factor = max(0, 1 - counter[W] / sum5)
    cdef float other_words_factor = sum(max(0, 1 - counter[w] / sum5) for w in main_dict[S])
    return word_factor / other_words_factor


cdef float affinity_WS(str W, str S):
    return latest_WSM[W][word_with_indices[S]].max()


cdef float affinity_SW(str S, str W):
    return latest_SSM[S][sentence_with_indices[W]].max()


cdef float similarity_W(str W1, str W2):
    return sum(weight(s, W1) * affinity_SW(s, W2)
               for s in s_include_word[W1])

cdef float similarity_S(str S1, str S2):
    return sum(weight(S1, w) * affinity_WS(w, S2)
               for w in main_dict[S1])

cdef void save_matrixs(name):
    np.save("SSM_{}.txt".format(name),
            latest_SSM)
    np.save("WSM_{}.txt".format(name),
            latest_WSM)

cdef void iteration(name):
    sent_comb = combinations(map(str, all_sent), 2)
    word_comb = combinations(map(str, all_words), 2)
    sent_comb = iter(tee(sent_comb, 4))
    word_comb = iter(tee(word_comb, 4))
    cdef int w_size = all_words.size
    cdef int s_size = all_sent.size
    cdef tuple ind_lower_s = np.tril_indices(s_size, -1)
    cdef tuple ind_uper_s = np.triu_indices(s_size, 1)
    cdef tuple ind_lower_w = np.tril_indices(w_size, -1)
    cdef tuple ind_uper_w = np.triu_indices(w_size, 1)
    cdef np.ndarray latest_SSM_view = latest_SSM.view(np.float16).reshape(s_size, -1)
    cdef np.ndarray latest_WSM_view = latest_WSM.view(np.float16).reshape(w_size, -1)
    for i in range(iteration_number):
        # Update SSM
        new_arr = np.array([similarity_S(s1, s2) for s1, s2 in next(sent_comb)]).astype(np.float16)
        latest_SSM_view[ind_uper_s] = new_arr
        latest_SSM_view[ind_lower_s] = new_arr
        print("Finished similarity_S, iteration {}".format(i + 1))
        # Update WSM
        new_arr = np.array([similarity_W(w1, w2) for w1, w2 in next(word_comb)]).astype(np.float16)
        latest_WSM_view[ind_uper_w] = new_arr
        latest_WSM_view[ind_lower_w] = new_arr
        print("Finished similarity_W, iteration {}".format(i + 1))

    save_matrixs(name)


def main():
    run()
