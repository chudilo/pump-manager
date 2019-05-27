from bs4 import BeautifulSoup as soup
import urllib.request
import logging

def chng_str(txt):
    #print(txt)
    pre_res = txt.split()
    #print(pre_res)
    if "Arcade" not in pre_res:
        return ""
        
    res = ""
    for word in pre_res:
        if word == "ID:":
            break
        res += word + ' '
    
    return res


def getSongs():
    logging.basicConfig(filename='history.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    url_songs = "https://pumpout.anyhowstep.com/songs/"

    #ПОФИКСИТЬ ЕСЛИ НЕТ ИНТЕРНЕТА
    songs = list()

    for i in range(1, 800):
        try:
            html = urllib.request.urlopen(url_songs + str(i))

            #print(html.read())
            page_soup = soup(html, 'html.parser')
            #print(page_soup.find_all('div', {'class':'media-body'}).text)
            parsed = page_soup.find('div', {'class':'media-body'})
            songs.append(parsed.text.split())
            print(songs[len(songs)-1])
        
        except urllib.error.HTTPError:
            logging.warning("HttpError")
        except Exception as e:
            logging.error(e)

    return songs


if __name__ == '__main__':
    getSongs()

'''
import os
import sqlite3

def createDataBase():
    os.remove("./pumpdb.sqlite")

    conn = sqlite3.connect('pumpdb.sqlite')
    curs = conn.cursor()

    curs.execute("""CREATE TABLE Player (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nickname VARCHAR)""")

    curs.execute("""CREATE TABLE Community (
                            idCommunity   INTEGER PRIMARY KEY,
                            nameCommunity VARCHAR
                            )""")

#    curs.execute

    curs.close()
    conn.close()

createDataBase()
'''

