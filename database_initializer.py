from SearchEngine.models import ServerNames
import json
import django
import os


class Initializer:
    def __init__(self, *args, **kwargs):
        self.file_name = kwargs['data_path']
        self.excluded_names = kwargs['excluded_names']

    def __call__(self):
        server_names = self.load_data()
        for name, url in server_names.items():
            if name not in self.excluded_names:
                query = ServerNames(name=name, path=url)
                query.add()

    def load_data(self):
        with open(self.file_name) as f:
            server_names = json.load(f)
            return server_names
