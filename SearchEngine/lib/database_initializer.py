from SearchEngine.models import ServerName, WordNet
from SearchEngine.lib.create_tables import create_servers
from os import path as ospath
import json
import glob


class Initializer:
    def __init__(self, *args, **kwargs):
        self.server_names_path = kwargs['data_path']
        self.excluded_names = kwargs['excluded_names']
        self.servers_path = kwargs['server_path']
        self.wordnet_path = kwargs['wordnet_path']
        self.server_names = self.load_server_names()

    def __call__(self):
        print("Initializing server_names...")
        self.add_server_names()
        print("Initializing wordnets...")
        self.add_wordnets()
        print("Initializing servers...")
        self.add_servers()

    def add_wordnets(self): 
        query = WordNet()
        for word, similars in self.load_wordnets().items():
            query.word = word
            query.set_similars(similars)
            query.save()

    def add_servers(self):
        servers = create_servers(server_names=self.server_names)
        for name, file in self.load_servers():
            model_ = servers[name]
            query = model_()
            for path, file_names in file.items():
                query.path = path
                query.set_file_names(file_names)
                query.save()

    def add_server_names(self):
        query = ServerName()
        for name, url in self.server_names.items():
            if name not in self.excluded_names:
                query.name = name
                query.path = url
                query.set_table_field(name)
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
