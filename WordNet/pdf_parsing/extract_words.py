import codecs
from collections import deque
from string import digits
from collections import OrderedDict
import json
import re


class Extractor(object):
    """Extractor class for extracting the words from the words files."""

    def __init__(self, *args, **kwargs):
        self.index_regex = re.compile(r'(Index\s*\d+)|(\d+\s*Index)')
        self.number_regex = re.compile(r'[\d\s,\W]+', re.U)
        self.digits = tuple(digits)
        self.words_file_name = kwargs["words_file_name"]
        self.json_file_name = kwargs['json_file_name']

    def pars_words(self):
        """Read the words file and refines the format of lines."""
        seen = deque()
        with codecs.open(self.words_file_name, encoding='UTF-8') as f:

            for line in f:
                line = line.strip()
                if self.index_regex.match(line):
                    continue

                if not seen:
                    if not line.endswith(self.digits):
                        if 'see' in line:
                            line = line.split('see')[0]
                        seen.append(line)

                    elif line.endswith(self.digits):
                        yield line
                    else:
                        raise Exception("seen is empty and the line is {}".format(repr(line)))
                else:
                    if self.number_regex.match(line) or line.endswith(self.digits):
                        if 'see' in line:
                            line = line.split('see')[0]
                        seen.append(line)
                        yield ''.join(seen)
                        seen.clear()

                    elif not line.endswith(digits):
                        seen.append(line)

                    else:
                        try:
                            raise Exception(u"seen is {} and the line is {}".format(seen,repr(line)))
                        except UnicodeEncodeError as e:
                            raise e

    def refine_numbers(self, nums):
        """Convert the numbers to integer an generate the numbers between a range."""
        for num in nums:
            try:
                if "\xe2\x80\x93" in num:
                    start, end = map(int, num.split('\xe2\x80\x93'))
                    for i in range(start, end + 1):
                        yield i
                else:
                    yield int(num)
            except ValueError:
                print "Num {} was escaped".format(num)

    def pars_lines(self):
        """
        Parsing the refined lines and create a dictionary withe the words
        as the key and the page numbers as a list of values.
        """
        words = OrderedDict()
        regex = re.compile(r'(?:(\d+)|(\d+\xe2\x80\x93\d+))(?=$|[, ])')
        for line in self.pars_words():
            numbers = regex.findall(line.encode('utf8'))
            numbers = [i if i else j for i, j in numbers]
            word = regex.sub('', line.encode('utf8')).strip(' ,')
            words[word] = list(self.refine_numbers(numbers))
        return words

    def create_json(self):
        words = self.pars_lines()
        with codecs.open(self.json_file_name, 'w', encoding='UTF-8') as f:
            json.dump(words, f, indent=4)


if __name__ == '__main__':

    Ex = Extractor(words_file_name='words.txt',
                   json_file_name='words.json')

    Ex.create_json()
