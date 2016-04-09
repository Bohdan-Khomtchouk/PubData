import json
from nltk import word_tokenize, pos_tag
import codecs


class Corpus():
    def __init__(self, *args, **kwargs):
        self.input_file = kwargs['input_file']
        self.output_file = kwargs['output_file']

    def create_dict(self):
        with codecs.open(self.input_file, encoding='UTF-8') as f:
            words = json.load(f)
        new_dict = {k: [word for word, tag in pos_tag(word_tokenize(v)) if tag == 'NN' and len(word)>3] for k, v in words.items()}
        return new_dict

    def create_json(self):
        tagged_dict = self.create_dict()
        with codecs.open(self.output_file, 'w', encoding='UTF-8') as f:
            json.dump(tagged_dict, f, indent=4)


if __name__ == "__main__":
    Crp = Corpus(input_file='pdf_parsing/final_result.json',
                 output_file='corpus.json')
    Crp.create_json()
