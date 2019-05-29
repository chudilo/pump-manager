import os
from celery import Celery
from django.conf import settings

# Indicate Celery to use the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings')
# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
'''
from __future__ import absolute_import
from celery import Celery
from django.conf import settings

#settings.configure()
from PumpManager.pumpdb import convertSongs, getMixes
import PumpManager.models


app = Celery("MY_TASKS", broker='amqp://localhost//', backend='rpc://')
#app.config_from_object('django.conf:settings')

# This line will tell Celery to autodiscover all your tasks.py that are in your app folders
#app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task
def add(x, y):
    print("HERE IS ASYNC WORK")
    return x + y

@app.task
def update_db():
    print("START UPDATING SONG DB")

    songs = convertSongs()
    for song in songs:
        print(song)
        s = Song(   name=song['name'],
                    author = song['author'],
                    bpm = song['bpm'],
                    type = song['type'],
                    cathegory = song['cathegory'],
                    )
        try:
            s.save()
        except:
            pass

        for chart in song['charts']:
            c = Chart(  lvl=chart['lvl'],
                        type=chart['type'],
                        song=s,
                        )
            try:
                c.save()
            except:
                pass
    print("END UPDATING SONG DB")
'''
