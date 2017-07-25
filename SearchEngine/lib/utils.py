# from django.db import models
# from django.contrib import admin
from sys import path as syspath
from os import path as ospath
from django.db.models import Q
# from collections import defaultdict
from string import punctuation, whitespace
# from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
import re

syspath.append(ospath.join(ospath.expanduser("~"), 'PubData'))
from SearchEngine.models import Server, WordNet


class FindSearchResult:
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs['keyword'].strip('-_')
        self.selected_servers = kwargs['servers']

    def validate_keyword(self):
        punct = set(punctuation) - {'-', '_'}
        cond1 = len(self.keyword) > 1
        cond2 = not punct.intersection(self.keyword)
        cond3 = not set(whitespace).intersection(self.keyword)

        result = cond1 and cond2 and cond3
        if result:
            lst = re.split(r'(-|_)', self.keyword)
            all_subs = {''.join(lst[i:j]) for i in range(0, len(lst) - 2, 2)
                        for j in range(i + 3, len(lst) + 2, 2)}
            self.all_valid_substrings = list(all_subs | {self.keyword})
            splitted_substrings = re.split(r'-|_', self.keyword)
            if len(splitted_substrings) > 1:
                self.splitted_substrings = splitted_substrings
            else:
                self.splitted_substrings = []
        return result

    def find_result(self):
        # query = Server()
        # query.objects.filter(name__in=selected_servers)
        if not self.validate_keyword():
            raise ValueError("Invalid Keyword")
        all_result = {}
        all_servers = {name: Server.objects.get(name=name) for name in self.selected_servers}
        wordnet_result = list(self.get_similars())
        for name, server in all_servers.items():
            result = []
            for path, files in server.data.items():
                for wn in wordnet_result:
                    if self.check_intersection(wn, files):
                        result.append({'path': path,
                                       'exact_match': self.keyword == wn['word']})
            all_result[name] = result

        return all_result

    def check_intersection(self, wn, files):
        # this should be done in json files
        corrected_file_names = [f.split('.')[0] for f in files]
        similars = wn['similars'] | {wn['word']}
        return any(any(s in f for s in similars) for f in corrected_file_names)

    def get_similars(self):
        cond1 = Q(similars__overlap=self.all_valid_substrings)
        cond2 = Q(word__in=self.all_valid_substrings)
        cond3 = Q(similars__overlap=self.splitted_substrings)
        all_obj = WordNet.objects.filter(cond1 | cond2 | cond3)
        for obj in all_obj:
            yield {'word': obj.word, 'similars': set(obj.similars)}
