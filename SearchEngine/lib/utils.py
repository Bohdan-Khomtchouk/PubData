from django.db import models
from django.contrib import admin
from sys import path as syspath
from os import path as ospath
from django.db.models import Q
from collections import defaultdict
syspath.append(ospath.join(ospath.expanduser("~"), 'PubData'))
from SearchEngine.models import Server, WordNet


class FindSearchResult:
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs['keyword']
        self.selected_servers = kwargs['servers']

    def find_result(self):
        # query = Server()
        # query.objects.filter(name__in=selected_servers)
        all_servers = {name: Server.objects.get(name=name) for name in self.selected_servers}
        wordnet_result = list(self.get_similars())
        for name, server in all_servers.items():
            result = defaultdict(list)
            for path, files in server.data.items():
                for wn in wordnet_result:
                    if wn['word'] in files or wn['similars'].intersection(files):
                        result[name].append({'paths': path,
                                             'exact_match': self.keyword == wn['word']})
            yield result

    def get_similars(self):
        # wordnet = WordNet()
        all_obj = WordNet.objects.filter(
            Q(similars__contains=[self.keyword]) | Q(word=self.keyword)
        )

        for obj in all_obj:
            yield {'word': obj.word, 'similars': set(obj.similars)}
