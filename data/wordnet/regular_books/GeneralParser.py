from gensim.models import Word2Vec, Phrases
from nltk.stem.lancaster import LancasterStemmer
from nltk import pos_tag
from itertools import dropwhile
from string import punctuation
import glob
import json


class WordNet:
    def __init__(self, min_count=3, size=100, window=14, **kwargs):
        self.model_path = kwargs['model_path']
        self.data_path = kwargs['data_path']
        self.wordnet_name = kwargs['wordnet_name']
        self.min_count = min_count
        self.size = size
        self.window = window

    def create_train_model(self):
        """ Create the trained model based on custom attributes."""
        st = LancasterStemmer()
        with open(self.data_path, encoding='utf8') as f_name:
            sentences = [[st.stem(w) for w, t in pos_tag(line.lower().split()) if 'N' in t] for line in f_name]
            sentences = [filter(lambda x: len(x) > 2, (word.strip(punctuation) for word in sentences)) for sent in sentences]
            model = Word2Vec(sentences,
                             min_count=self.min_count,
                             size=self.size,
                             window=self.window,
                             workers=4)
            model.save(self.model_path)

    def load_model(self):
        """load the model."""
        model = Word2Vec.load(self.model_path)
        return model

    def create_wordnet(self):
        model = self.load_model()
        with open("{}.json".format(self.wordnet_name), 'w') as f:
             json.dump({w: next(zip(*model.wv.similar_by_word(w, topn=20))) \
             for w in model.wv.vocab.keys() }, f, indent=4)
