from django.db import models
from django.utils import timezone
from djangotoolbox.fields import ListField


class Database(models.Model):
    name = models.CharField(max_length=200)
    path = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class ServerNames(models.Model):
	name = models.CharField(max_length=200)
	path = models.TextField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class WordNet(models.Model):
	word = models.CharField(max_length=200)
	similars = models.TextField(max_length=200)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
