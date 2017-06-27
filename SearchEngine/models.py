from django.db import models
from django.utils import timezone
import json


class Server(models.Model):
    path = models.CharField(max_length=200)
    files = models.TextField()
    creation_date = models.DateTimeField(
            default=timezone.now)

    def set_files(self, args):
        self.files = json.dumps(args)

    def get_files(self):
        return json.loads(self.foo)

    def add(self):
        self.creation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ServerNames(models.Model):
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    creation_date = models.DateTimeField(
            default=timezone.now)

    def add(self):
        self.creation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "name: {} | path: {}".format(self.name, self.path)


class WordNet(models.Model):
    word = models.CharField(max_length=200)
    similars = models.TextField()

    def set_similars(self, args):
        self.files = json.dumps(args)

    def get_similars(self):
        return json.loads(self.foo)

    def add(self):
        # self.published_date = timezone.now()
        self.save()

class Recommendation(models.Model):
    user = models.ForeignKey('auth.User')
    recom = models.TextField()

    def set_recoms(self, args):
        self.files = json.dumps(args)

    def get_recoms(self):
        return json.loads(self.foo)

    def add(self):
        # self.published_date = timezone.now()
        self.save()