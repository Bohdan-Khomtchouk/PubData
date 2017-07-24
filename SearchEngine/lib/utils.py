from django.db import models
from django.contrib import admin
from sys import path as syspath
from os import path as ospath
from django.db.models import Q
from collections import defaultdict
syspath.append(ospath.join(ospath.expanduser("~"), 'PubData'))
from SearchEngine.models import Server, WordNet
from string import punctuation, whitespace


class FindSearchResult:
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs['keyword']
        self.selected_servers = kwargs['servers']

    def validate_keyword(self):
        punctuation = set(punctuation) - {'-', '_'}
        cond1 = len(self.kwargs) > 1
        cond2 = not punctuation.intersection(self.keyword)
        cond3 = not set(whitespace).intersection(self.keyword)

        return cond1 and cond2 and cond3

    def find_result(self):
        # query = Server()
        # query.objects.filter(name__in=selected_servers)
        if not self.validate_keyword():
            # should raise exception
            return []
        all_servers = {name: Server.objects.get(name=name) for name in self.selected_servers}
        wordnet_result = self.get_similars()
        for name, server in all_servers.items():
            result = defaultdict(list)
            for path, files in server.data.items():
                print ([path, files])
                for wn in wordnet_result:
                    print(wn)
                    if self.check_intersection(wn, files):
                        result[name].append({'paths': path,
                                             'exact_match': self.keyword == wn['word']})
            yield result

    def check_intersection(self, wn, files):
        if any(wn['word'] for f in files) or wn['similars'].intersection(files):
    
    def get_similars(self):
        # wordnet = WordNet()
        all_obj = WordNet.objects.filter(
            Q(similars__contains=[self.keyword]) | Q(word=self.keyword)
        )

        for obj in all_obj:
            yield {'word': obj.word, 'similars': set(obj.similars)}
