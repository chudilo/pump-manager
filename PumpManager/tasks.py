from celery.decorators import task
from testproj.clr import app as celery_app
from PumpManager.models import Song, Chart, Mix
from PumpManager.pumpdb import getSong
import logging

logging.basicConfig(filename='history.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

@celery_app.task(name = "upgr_db")
def upgr_db():
    print("START UPDATING SONG DB")
    song = "default"
    chart = "default"
    for i in range(1, 800):
        song = getSong(i)
        if song:
            try:
                print(song)
                #print(song['name'], song['author'], song['bpm'], song['type'], song['cathegory'])
                s = Song(   name=song['name'],
                            author = song['author'],
                            bpm = int(float(song['bpm'])),
                            type = song['type'],
                            cathegory = song['cathegory'],
                            )
                try:
                    s.save()
                except Exception as e:
                    logging.error(e)
                    logging.error(song)

                for mix in song['mixes']:
                    print(mix)
                    s.mix.add(Mix.objects.get(name = mix))
                    s.save()

                for chart in song['charts']:
                    c = Chart(  lvl=chart['lvl'],
                                type=chart['type'],
                                song=s,
                                )
                    try:
                        c.save()
                    except Exception as e:
                        logging.error(e)
                        logging.error(chart)

            except Exception as e:
                logging.warning("Cycle")
                logging.error(song)
                logging.error(chart)
                logging.error(e)

    print("END UPDATING SONG DB")

if __name__ == "__main__":
    upgr_db()
