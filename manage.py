#!/usr/bin/env python
import os
import sys
import django


if __name__ == "__main__":
    run_initializer = True
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PubData.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    else:
        if run_initializer:
            django.setup()
            from SearchEngine.lib import database_initializer
            excluded_names = {"The Arabidopsis Information Resource",
                              "O-GLYCBASE",
                              "PairsDB",
                              "Gene Expression Omnibus",
                              "One Thousand Genomes Project",
                              "GenBank",
                              "Sequence Read Archive"}
            initializer = database_initializer.Initializer(data_path='data/servernames.json',
                                                           server_path='data/json_files',
                                                           wordnet_path='data/wordnet',
                                                           excluded_names=excluded_names)
            initializer()
            run_initializer = False
    execute_from_command_line(sys.argv)
