from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone


class SearchQuery(models.Model):
    user = models.ForeignKey('auth.User')
    word = models.CharField(max_length=100)
    servers = ArrayField(models.CharField(max_length=100, blank=True))
    search_date = models.DateTimeField(default=timezone.now)

    def add(self, **kwargs):
        self.search_date = timezone.now()
        self.word = kwargs['word']
        self.servers = kwargs['servers']
        self.save()

    def __str__(self):
        return self.word


class Server(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    data = JSONField()

    def __str__(self):
        return self.name


class Path(models.Model):
    path = models.TextField()
    files = ArrayField(models.CharField(max_length=300))
    keywords = ArrayField(models.CharField(max_length=100))
    server_name = models.CharField(max_length=50)
    metadata = models.CharField(max_length=200)

    def __str__(self):
        return self.path


class ServerName(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    server = models.OneToOneField(Server,
                                  on_delete=models.CASCADE,
                                  primary_key=True,)
    creation_date = models.DateTimeField(default=timezone.now)

    def add(self):
        self.creation_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def __repr__(self):
        return "name: {} | path: {}".format(self.name, self.path)


class WordNet(models.Model):
    word = models.CharField(max_length=200)
    similars = ArrayField(models.CharField(max_length=200, blank=True))

    def __str__(self):
        return self.word
    
    def add(self):
        self.save()


class Recommendation(models.Model):
    user = models.OneToOneField('auth.User')
    recommendations = JSONField()

    def __str__(self):
        return str(self.user)
