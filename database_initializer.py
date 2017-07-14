from SearchEngine.models import ServerNames, WordNet
import json
import glob


class Initializer:
    def __init__(self, *args, **kwargs):
        self.server_path = kwargs['data_path']
        self.excluded_names = kwargs['excluded_names']

    def __call__(self):
        pass

    def add_wordnets(self): 
        query = WordNet()
        for word, similars in self.load_wordnets():
            query.word = word
            query.add_similars(similars)
            query.save()

    def add_servers(self):
        pass

    def add_server_names(self):
        server_names = self.load_servers()
        query = ServerNames()
        for name, url in server_names.items():
            if name not in self.excluded_names:
                query.name = name
                query.path = url
                query.add()

    def load_servers(self):
        with open(self.server_path) as f:
            server_names = json.load(f)
            return server_names

    def load_wordnets(self):
        all_wordnets = {}
        for f_name in glob.glob(self.wordnet_path):
            with open(f_name) as f:
                all_wordnets.update(json.load(f))
        return all_wordnets

