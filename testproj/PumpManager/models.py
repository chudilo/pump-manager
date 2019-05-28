from django.db import models
from django.contrib.auth.models import User

#from django.conf import settings
#settings.configure()

# Create your models here.

class Mix(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class Version(models.Model):
    version = models.CharField(max_length=10)
    mix = models.ForeignKey(Mix, on_delete=models.CASCADE)
    def __str__(self):
        return self.mix.name + ": " + self.version


class Location(models.Model):
    name = models.CharField(max_length=40)

    address = models.CharField(null = True, max_length=150)
    game = models.ManyToManyField(Mix, null=True, blank=True)
#null has no effect on many to many field

class Community(models.Model):
    name = models.CharField(max_length=25)

    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)


class Player(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=25)

    community = models.ForeignKey(Community, null=True, blank=True, on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.nickname


class Song(models.Model):
    name = models.CharField(max_length=40, unique="True")
    author = models.CharField(max_length=40)

    bpm = models.IntegerField()
    type = models.CharField(max_length=40)
    cathegory = models.CharField(max_length=40)
    version = models.ForeignKey(Version, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Chart(models.Model):
    lvl = models.IntegerField()

    type = models.CharField(max_length=40)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    def __str__(self):
        return self.song.name + ": " + self.type+"-lvl"+str(self.lvl)

class Stage(models.Model):
    score = models.CharField(max_length=15)
    grade = models.CharField(max_length=4)

    time = models.DateTimeField()
    chart = models.ForeignKey(Chart, null=True, on_delete=models.SET_NULL)
    player = models.ForeignKey(Player, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.chart.song.name + " - " +\
        self.chart.type + str(self.chart.lvl) + ": " +\
        self.grade + " - " + self.score
