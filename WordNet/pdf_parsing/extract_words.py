#!/usr/bin/env python

# Copyright (C) 2015-2016 Bohdan Khomtchouk, Kasra Ahmadvand, Thor Wahlestedt, Grant Kimes, Kelly Khomtchouk, Vytas Dargis-Robinson, Claes Wahlestedt

# PubData is a genomics search engine and file retrieval system for all bioinformatics databases worldwide.  PubData searches biomedical FTP data in a user-friendly fashion similar to how PubMed searches biomedical literature.  PubData is hosted as a standalone GUI software program, while PubMed is hosted as an online web server.  PubData is built on novel network programming and natural language processing algorithms that can patch into the FTP servers of any user-specified bioinformatics database, query its contents, and retrieve files for download.
# Future plans include adding web server support for PubData, and contributions from the open source community are welcome.
# PubData is designed as a graphical user interface (GUI) software program written in the Python programming language and PySide (Python binding of the cross-platform GUI toolkit Qt).  PubData can remotely search, access, view, and retrieve files from the deeply nested directory trees of any major bioinformatics database via a local computer network.  
# By assembling all major bioinformatics databases under the roof of one software program, PubData allows the user to avoid the unnecessary hassle and non-standardized complexities inherent to accessing databases one-by-one using an Internet browser.  More importantly, it allows a user to query multiple databases simultaneously for user-specified keywords (e.g., `human`, `cancer`, `transcriptome`).  As such, PubData allows researchers to search, access, view, and retrieve files from the FTP servers of any major bioinformatics database directly from one centralized location.  By using only a GUI, PubData allows the user to simultaneously surf multiple bioinformatics FTP servers directly from the comfort of their local computer.
# PubData is an ongoing bioinformatics software project financially supported by the United States Department of Defense (DoD) through the National Defense Science and Engineering Graduate Fellowship (NDSEG) Program. This research was conducted with Government support under and awarded by DoD, Army Research Office (ARO), National Defense Science and Engineering Graduate (NDSEG) Fellowship, 32 CFR 168a.
# Please cite: "Khomtchouk et al.: 'PubData: genomics search engine for bioinformatics databases', 2016 (in preparation)" within any source that makes use of any methods inspired by PubData.
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -------------------------------------------------------------------------------------------

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
        """Read the words file and refine the format of lines."""
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
        """Convert the numbers to integer and generate the numbers between a range."""
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
        Parsing the refined lines and create a dictionary with the words
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
