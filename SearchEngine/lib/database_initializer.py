from sys import path as syspath
from os import path as ospath, environ
from django import setup
import json
import glob
import re
from string import punctuation
from django.db import transaction
syspath.append(ospath.join(ospath.expanduser("~"), 'Airportbio'))
environ.setdefault("DJANGO_SETTINGS_MODULE", "Airport.settings")
setup()
from SearchEngine.models import ServerName, WordNet, Server, Path


class Initializer:
    def __init__(self, *args, **kwargs):
        self.server_names_path = kwargs['data_path']
        self.excluded_names = kwargs['excluded_names']
        self.servers_path = kwargs['server_path']
        self.wordnet_path = kwargs['wordnet_path']
        self.metadata_links = self.load_metadata(kwargs['metadata'])
        self.server_names = self.load_server_names()
        self.punc_regex = re.compile(r'[{}]'.format(re.escape(punctuation)))

    def __call__(self):
        print("Initializing wordnets...")
        self.add_wordnets()
        print("Initializing server_names...")
        self.add_server_names()

    def load_metadata(self, filepath):
        with open(filepath) as f:
            return json.load(f)

    def add_wordnets(self): 
        all_models = []
        for word, similars in self.load_wordnets().items():
            query = WordNet()
            query.word = word
            query.similars = similars
            all_models.append(query)
        WordNet.objects.bulk_create(all_models)
    
    @transaction.atomic
    def initial_path_model(self, name, data):
        for d in data:
            path = Path()
            path.path = d['path']
            path.files = d['files']
            path.keywords = d['keywords']
            path.metadata = self.metadata_links[name]
            path.server_name = name
            path.save()

    def create_server_models(self):
        all_models = {}
        for name, data in self.load_servers():
            self.initial_path_model(name, data)
            query = Server()
            query.name = name
            query.data = data
            all_models[name] = query
        return all_models

    @transaction.atomic
    def add_server_names(self):
        query = ServerName()
        all_models = self.create_server_models()
        for name, url in self.server_names.items():
            if name not in self.excluded_names:
                query.name = name
                query.path = url
                server_model = all_models[name]
                server_model.url = url
                server_model.save()
                query.server = server_model
                query.add()

    def load_server_names(self):
        with open(self.server_names_path) as f:
            server_names = json.load(f)
            return server_names

    def load_wordnets(self):
        all_wordnets = {}
        for f_name in glob.glob(self.wordnet_path + '/*.json'):
            with open(f_name) as f:
                all_wordnets.update(json.load(f))
        return all_wordnets

    def load_servers(self):
        for f_name in glob.glob(self.servers_path + '/*.json'):
            with open(f_name) as f:
                yield ospath.splitext(f_name)[0].split('/')[-1], json.load(f)


if __name__ == '__main__':
    excluded_names = {"The Arabidopsis Information Resource",
                      "O-GLYCBASE",
                      "PairsDB",
                      "Gene Expression Omnibus",
                      "One Thousand Genomes Project",
                      "GenBank",
                      "Sequence Read Archive"}
    initializer = Initializer(data_path='data/servernames.json',
                              server_path='data/refined_json_files',
                              wordnet_path='data/wordnet/dictionary_book/final_results',
                              metadata='data/metadata.json',
                              excluded_names=excluded_names)
    initializer()
