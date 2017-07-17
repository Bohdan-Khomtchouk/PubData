from SearchEngine.lib.utils import create_model
from django.db import models
import django
import os
import json
from django.core.management import call_command
from django.db import connection


def create_servers(server_names):
    def set_file_names(cls, args):
        cls.file_names = json.dumps(args)

    def get_file_names(cls):
        return json.loads(cls.file_names)
    cache = {}
    for name in server_names:
        model_class = create_model(name,
                                   fields={'path': models.CharField(max_length=200),
                                           'file_names': models.TextField(),
                                           'set_file_names': set_file_names,
                                           'get_file_names': get_file_names,
                                           '__str__': lambda self: self.__name__},
                                   app_label='SearchEngine',
                                   module='SearchEngine.models',
                                   options=None,
                                   admin_opts={})

        cache[name] = model_class
        # with connection.schema_editor() as editor:
        #    editor.create_model(model_class)
    return cache

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PubData.settings")
    django.setup()
    create_servers('data/servernames.json')
