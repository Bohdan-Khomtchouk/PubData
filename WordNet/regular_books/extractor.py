# -*- coding: utf-8 -*-


from nltk import pos_tag
from nltk.stem import LancasterStemmer, PorterStemmer, RegexpStemmer
from string import punctuation
import json
import glob
import re


def stemming(word):
    # Use stemmers for removing morphological affixes from words.
    Portst = PorterStemmer()
    Landst = LancasterStemmer()
    Regst = RegexpStemmer('ing|ed')
    new = Portst.stem(word)
    if new == word:
        new = Landst.stem(word)
        if new == word:
            new = Regst.stem(word)
    return new


def refine_data(main_dict):
    regex1 = re.compile(r'[a-zA-Z]', re.U)
    regex2 = re.compile(r'[^a-zA-Z]', re.U)
    regex3 = re.compile(r'[^\w]*(\w+)[^\w]*$', re.U)

    def check_word(w):
        a = not bool({"*", "+", "/", ","}.intersection(w))
        b = len(regex1.findall(w)) > 2
        c = not(len(regex2.findall(w)) > 2)
        d = 2 < len(w) < 20
        f = not w.endswith('ing')
        g = not w.endswith('-')
        return all([a, b, c, d, f])

    result = {k: {regex3.search(w).group(1) for w in v if check_word(w)}
              for k, v in main_dict.items() if v}
    result = {k: [w.replace(u'ﬁ', 'fi').replace(u'ﬂ', 'fl').replace(u'ϫ', 'j') for w in v if check_word(w)] for k, v in result.items() if v}
    return {str(k): v for k, v in result.items() if v}


def create_jsons():
    for file_name in glob.glob("files/*.txt"):
        result = {}
        with open(file_name) as f:
            content = f.read()
            paragraphs = filter(bool, {p.strip() for p in re.split(r'\n+', content)})
            for p in paragraphs:
                if not p.startswith('Figure'):
                    sentences = re.split(r'[.,]', p)
                    if len(sentences) > 2:
                        for sent in sentences:
                            sent.replace(r'-\n', '')
                            result.update({hash(sent): filter(bool, re.split(r'\s', sent))})

        total = {}
        for k, v in result.items():
            if len(v) > 1:
                value = {stemming(w.strip(punctuation).lower().decode('utf8', 'replace')) for w, tag in pos_tag(v) if 'NN' in tag and len(w) > 2}
                if value:
                    total[k] = list(value)

        with open("{}.json".format(file_name.split('.')[0]), 'w') as f:
            json.dump(refine_data(total), f, indent=4)


create_jsons()
