from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import JSONField


class Session(models.Model):
    name_session = models.CharField(max_length=30, default='0')
    matrix = JSONField(default=list)
    player_one = models.CharField(max_length=30, default='0')
    player_two = models.CharField(max_length=30, default='0')

    def set_name(self, name_session):
        self.name_session = name_session

    def set_matrix(self, matrix):
        self.matrix = matrix

    def get_matrix(self):
        return self.matrix

    def __str__(self):
        return f"{self.name_session}"


class Users(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.login
