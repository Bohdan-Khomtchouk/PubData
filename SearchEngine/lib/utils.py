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
from SearchEngine.models import Server, WordNet, Path


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
        wordnet_result = self.get_similars()
        all_words = wordnet_result['words'] & wordnet_result['similars']
        print(wordnet_result)
        for name, url in self.selected_servers.items():
            cond1 = Q(server_name=name)
            # cond2 = Q(files__overlap=list(wordnet_result['similars']))
            # cond3 = Q(files__overlap=list(wordnet_result['words']))
            query_result = Path.objects.filter(cond1)  # & (cond2 | cond3))
            result = [{'path': obj.path,
                       'exact_match': self.keyword in wordnet_result['words']}
                      for obj in query_result if self.check_intersection(obj, all_words)]

            all_result[name] = {'data': result,
                                'url': url}

        return all_result

    def check_intersection(self, obj, all_words):
        # this should be done in json files
        return any(self.keyword in word or any(i in word for i in self.splitted_substrings)
                   for word in all_words)

    def get_similars(self):
        cond1 = Q(similars__overlap=self.all_valid_substrings)
        cond2 = Q(word__in=self.all_valid_substrings)
        cond3 = Q(similars__overlap=self.splitted_substrings)
        all_obj = WordNet.objects.filter(cond1 | cond2 | cond3)
        words = {obj.word for obj in all_obj}
        similars = {i for obj in all_obj for i in obj.similars}
        return {'words': words, 'similars': similars}
