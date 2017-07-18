from django.db import models
from django.contrib import admin
from sys import path as syspath
from os import path as ospath
syspath.append(ospath.join(ospath.expanduser("~"), 'PubData'))
from SearchEngine.models import Server


def find_search_result(**kwargs):
    keyword = kwargs['keyword']
    servers = kwargs['servers']
