from django.db import models


# Create your models here.

class Article(models.Model):
    label = models.CharField(max_length=200)
    body = models.TextField(max_length=200)
    datePublish = models.DateTimeField()
    author = models.CharField(max_length=200, default="")

    def setBody(self, body):
        self.body = body

    def setAuthor(self, author):
        self.author = author

    def setLabel(self, label):
        self.label = label

    def setDatePublish(self, datePublish):
        self.datePublish = datePublish

    def getBody(self):
        return self.body

    def getLabel(self):
        return self.label

    def getDatePublish(self):
        return self.datePublish

    def getAuthor(self):
        return self.author

    def __str__(self):
        return self.label
