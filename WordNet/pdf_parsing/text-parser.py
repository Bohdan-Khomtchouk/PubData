import json
from collections import OrderedDict
import codecs
from xml.etree import ElementTree
from itertools import chain
from operator import itemgetter



class Mainparser():
    def __init__(self, *args, **kwargs):
        self.json_file_name = kwargs['jfn']
        self.xml_file_name = kwargs['xfn']

    def read_word_josn(self):
        with open(self.json_file_name) as f:
            return json.load(f)

    def pager(self):
        with open(self.xml_file_name) as f:
            tree = ElementTree.parse(f)
        root = tree.getroot()
        for neighbor in root.iter('page'):
            sub = [[node.text] if node.text else [sub.text + ' ' if sub.text else '' for sub in node.getchildren()] for node in neighbor.getchildren()]
            sub = chain.from_iterable(sub)
            if neighbor.text:
                yield (int(neighbor.get('number')) - 17, neighbor.text + ''.join(sub))

    def create_dict(self):
        return OrderedDict(self.pager())

    def new_dict(self):
        words = self.read_word_josn()
        new_dict = {}
        for k, v in words.items():
            for i in v:
                new_dict.setdefault(i, []).append(k)
        return new_dict

    def combiner(self):
        text_dict = self.create_dict()
        words_dict = self.new_dict()
        new_dict = OrderedDict()
        for k, v in text_dict.items():
            new_dict.update({tuple(words_dict.get(k, '')): v})
        return new_dict

    def splitter(self):
        word_text = self.combiner()
        for words, text in word_text.items():
            pairs = sorted([(word, text.find(word)) for word in words], key=itemgetter(1)) + [('', None)]
            pairs = [(word, index) for word, index in pairs if index != -1]
            all_slices = [(word, text[index + len(word):next_ind]) for (word, index), (_, next_ind) in zip(pairs, pairs[1:])]
            yield all_slices

    def create_json(self):
        words = OrderedDict(chain.from_iterable(self.splitter()))
        # words = OrderedDict(chain(self.pager()))
        with codecs.open('pages.json', 'w', encoding='UTF-8') as f:
            json.dump(words, f, indent=4)


if __name__ == '__main__':
    MP = Mainparser(xfn='Encyclopedia_of_Biology_pages.xml',
                    jfn='words.json')

    MP.create_json()