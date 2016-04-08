import json
from nltk import word_tokenize, pos_tag
import codecs


def create_dict():
    with codecs.open('pdf_parsing/final_result.json', encoding='UTF-8') as f:
        words = json.load(f)
    new_dict = {k: [word for word, tag in pos_tag(word_tokenize(v)) if tag == 'NN'] for k, v in words.items()}
    return new_dict

def create_json():
    tagged_dict = create_dict()
    with codecs.open('corpus.json', 'w', encoding='UTF-8') as f:
        json.dump(tagged_dict, f, indent=4)

create_json()
