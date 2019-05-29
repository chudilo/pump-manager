from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from datetime import datetime
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

    sex = (models).CharField(max_length=1, default="M")
    def __str__(self):
        return self.nickname
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(sender)
        print(instance)
        print(created)
        print(**kwargs)
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()
'''

class Song(models.Model):
    name = models.CharField(max_length=40, unique="True")
    author = models.CharField(max_length=40)

    bpm = models.IntegerField()
    type = models.CharField(max_length=40)
    cathegory = models.CharField(max_length=40)
    mix = models.ManyToManyField(Mix)

    def __str__(self):
        return self.name

class Chart(models.Model):
    lvl = models.IntegerField()

    type = models.CharField(max_length=40)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    def __str__(self):
        if self.lvl%10 != self.lvl:
            return self.song.name + ": " + self.type+"-"+str(self.lvl)
        else:
            return self.song.name + ": " + self.type+"-0"+str(self.lvl)

class Stage(models.Model):
    score = models.CharField(max_length=15)
    grade = models.CharField(max_length=4)

    time = models.DateTimeField(default=datetime.now, blank=True)
    chart = models.ForeignKey(Chart, null=True, on_delete=models.SET_NULL)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    url = models.CharField(max_length=150, null = True, blank = True)

    def __str__(self):
        return self.chart.song.name + " - " +\
        self.chart.type + str(self.chart.lvl) + ": " +\
        self.grade + " - " + self.score
