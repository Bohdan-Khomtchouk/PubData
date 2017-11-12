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
        self.splitted_substrings = []
        self.punc_regex = re.compile(r'[{}]'.format(re.escape(punctuation)))

    def validate_keyword(self):
        punct = set(punctuation) - {'-', '_'}
        cond1 = len(self.keyword) > 1
        cond2 = not punct.intersection(self.keyword)

        result = cond1 and cond2
        if cond1 and cond2:
            lst = set([i for i in re.split(r'-|_', self.keyword) if i][:5])
            # all_subs = {''.join(lst[i:j]) for i in range(0, len(lst) - 2, 2)
            #            for j in range(i + 3, len(lst) + 2, 2)}
            splitted_substrings = list(lst | {self.keyword})
            if len(splitted_substrings) >= 1:
                self.splitted_substrings = splitted_substrings

        return result

    def find_result(self):
        # query = Server()
        # query.objects.filter(name__in=selected_servers)
        if not self.validate_keyword():
            raise ValueError("Invalid Keyword")
        wordnet_result = self.get_similars()
        all_words = wordnet_result['words'] & wordnet_result['similars']
        all_words = all_words.union(self.splitted_substrings)
        for name, url in self.selected_servers.items():
            cond1 = Q(server_name=name)
            # these conditions take too long
            # cond2 = Q(files__overlap=all_words)
            # cond3 = Q(path__icontains=all_words)
            query_result = Path.objects.filter(cond1)  # & (cond2 | cond3))
            for obj in query_result:
                if self.check_intersection(obj.files, obj.path, all_words):
                    yield {'path': obj.path,
                           'name': name,
                           'url': url,
                           'exact_match':self.exact_match(obj.files, obj.path) }

    
    def exact_match(self, files, path):
        return any(i in files or i in path for i in self.splitted_substrings)
    
    def check_intersection(self, files, path, all_words):
        # this should be done in json files
        files = {i for f in files for i in self.punc_regex.split(f)}
        return all_words.intersection(files) or any(i in path for i in all_words)
    
    def get_similars(self):
        cond1 = Q(similars__overlap=self.splitted_substrings)
        cond2 = Q(word__in=self.splitted_substrings)
        all_obj = WordNet.objects.filter(cond1 | cond2)
        words = {obj.word for obj in all_obj}
        similars = {i for obj in all_obj for i in obj.similars}
        return {'words': words, 'similars': similars}
