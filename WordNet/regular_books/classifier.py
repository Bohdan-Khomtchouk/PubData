import numpy as np
from itertools import combinations
from collections import defaultdict
from operator import itemgetter
import json
import re
import glob


regex = re.compile(r'[^_]+_([^.]+)\..*')
d = defaultdict(dict)
N = 10


def load_files():
    """Load arrays from files."""
    for name in glob.glob("*.npy"):
        file_name = regex.match(name).group(1)

        if name.startswith("WSM"):
            d[file_name]['WSM'] = np.load(name)
        elif name.startswith("SSM"):
            d[file_name]['SSM'] = np.load(name)
        elif name.startswith("sentences"):
            d[file_name]['sentences'] = np.load(name)
        elif name.startswith("words"):
            d[file_name]['words'] = np.load(name)

    for name, matrices in d.items():
        print(name)
        WSM = matrices['WSM']
        words = matrices['words']
        indices = np.argpartition(WSM, -N, axis=1)[:, -N:]
        # x = WSM.shape[0]
        # values = WSM[np.repeat(np.arange(x), N), indices.ravel()].reshape(x, N)
        # print(values)
        classified_words = {}
        for w, inds in zip(words, indices):
            classified_words[w] = list(words[inds])
        yield name, classified_words


result = load_files()

for name, dict_obj in result:
    with open("{}.json".format(name), 'w') as f:
        json.dump(dict_obj, f, indent=4)
