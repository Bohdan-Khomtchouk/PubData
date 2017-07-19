from django.db import models
from django.contrib import admin
from sys import path as syspath
from os import path as ospath
from django.db.models import Q
syspath.append(ospath.join(ospath.expanduser("~"), 'PubData'))
from SearchEngine.models import Server, WordNet


class FindSearchResult:
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs['keyword']
        self.selected_servers = kwargs['servers']

    def find_result(self):
        query = Server()
        # query.objects.filter(name__in=selected_servers)
        all_servers = {name: query.objects.get(name=name) for name in self.selected_servers}
        wordnet_result = self.get_similars()
        for name, server in all_servers:
            for path, files in server.data.items():
                for word in wordnet_result:
                    if any(word in f_name for f_name in files):
                        yield {'server': name,
                               'path': path,
                               'exact_match': self.keyword == word}

    def get_similars(self):
        wordnet = WordNet()
        obj = wordnet.objects.filter(
            Q(similars__contains=[self.keyword]) | Q(word=self.keyword)
        )
        if obj:
            return {'word': obj.word, 'similars': obj.similars}
