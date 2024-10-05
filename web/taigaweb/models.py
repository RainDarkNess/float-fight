from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import JSONField


class Session(models.Model):
    name_session = models.CharField(max_length=30, default='0')
    matrix = JSONField(default=list)

    player_one = models.CharField(max_length=30, default='ИГРОК ОТСУСТВУЕТ')
    player_two = models.CharField(max_length=30, default='ИГРОК ОТСУСТВУЕТ')

    matrix_player_two = JSONField(default=list)

    ship_count_player_one = models.IntegerField(default=0)
    ship_count_player_two = models.IntegerField(default=0)

    def set_name(self, name_session):
        self.name_session = name_session

    def set_matrix(self, matrix):
        self.matrix = matrix

    def set_matrix_player_two(self, matrix_player_two):
        self.matrix_player_two = matrix_player_two

    def get_matrix(self):
        return self.matrix

    def get_matrix_player_two(self):
        return self.matrix_player_two

    def set_player_one(self, player_one):
        self.player_one = player_one

    def set_player_two(self, player_two):
        self.player_two = player_two

    def set_ship_count_player_one(self, ship_count_player_one):
        self.ship_count_player_one = int(ship_count_player_one)

    def set_ship_count_player_two(self, ship_count_player_two):
        self.ship_count_player_two = int(ship_count_player_two)

    def get_ship_count_player_one(self):
        return self.ship_count_player_one

    def get_ship_count_player_two(self):
        return self.ship_count_player_two

    def get_room_name(self):
        return self.name_session

    def get_name_player_one(self):
        return self.player_one

    def get_name_player_two(self):
        return self.player_two

    def __str__(self):
        return f"{self.name_session}"


class restartCode(models.Model):
    restart_code = models.CharField(max_length=4)

    def addCode(self, restart_code):
        self.restart_code = restart_code

    def __str__(self):
        return f"{self.restart_code}"


class Users(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, default='')

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def set_username(self, username):
        self.login = username

    def get_username(self):
        return self.login

    def setEmail(self, email):
        self.email = email

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.login


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
