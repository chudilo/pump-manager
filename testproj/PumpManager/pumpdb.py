from bs4 import BeautifulSoup as soup
import urllib.request
import logging

import re

def chng_str(txt):
    #print(txt)
    pre_res = txt.split()
    #print(pre_res)

    res = ""
    for word in pre_res:
        if word == "ID:":
            break
        res += word + ' '

    return res


def chng_mix(txt):
    #print(txt)
    pre_res = txt.split()
    #print(pre_res)
    if pre_res[0] =='-':
        return ""

    res = ""
    for word in pre_res:
        if word == "-":
            break
        res += word + ' '

    return res


def getSongs(q):
    logging.basicConfig(filename='history.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    url_songs = "https://pumpout.anyhowstep.com/songs/"

    #ПОФИКСИТЬ ЕСЛИ НЕТ ИНТЕРНЕТА
    songs = list()
    charts = list()
    #for i in range(1, 800):
    for i in range(q,q+1):
        try:
            html = urllib.request.urlopen(url_songs + str(i))
            #print(html.read())
            page_soup = soup(html, 'html.parser')
            #print(page_soup.find_all('div', {'class':'media-body'}).text)
            parsed = page_soup.find('div', {'class':'media-body'})
            songs.append(parsed.text.split())
    #        print(songs[len(songs)-1])

            parsed = page_soup.find_all('img', {'class':'thumb pull-left'})
            #print(parsed)
            chart_dict = list()
            for pars in parsed:
    #            print(pars['src'])
                chart_dict.append(
                {'lvl' : pars['src'][15:][:-4][-2:],
                'type':  re.search("/\w{1,4}/", pars['src']).group()[1:-1]})

            #print(chart_dict)
            charts.append(chart_dict)



        except urllib.error.HTTPError:
            logging.warning("HttpError")
        except Exception as e:
            logging.error(e)


    '''
    for song in songs:
        print(song)
    for chart in charts:
        print(chart)
    '''
    return songs, charts

def convertSongs(q):
    songs, charts = getSongs(q)
    res = list()

    for i in range(len(songs)):
        song = dict()
        song['name'] = ''

        song['charts'] = charts[i]
        for j in range(len(songs[i])):
            if songs[i][j] != "ID:":
                song['name'] += songs[i][j] + ' '
            else:
                for k in range(j+2,len(songs[i])):
                    if songs[i][k] == "BPM":#.isdigit() or re.search("/\d{1,3}.?\d{0,3}/", pars['src']).group()[1:-1]:
                        song['author'] = ''
                        for l in range(k-j-3):
                            song['author'] += songs[i][j+2+l] + ' '
                        song['bpm'] = songs[i][k-1]
                        song['type'] = songs[i][k+1]
                        song['cathegory'] = songs[i][k+2]
                break

    for song in songs:
        print(song)

    #    print()
    res.append(song)

    return res

def getMixes():
    logging.basicConfig(filename='history.log', format='%(asctime)s; %(levelname)s:%(message)s', level=logging.DEBUG)

    url_mixes = "https://pumpout.anyhowstep.com/mixes/"

    #ПОФИКСИТЬ ЕСЛИ НЕТ ИНТЕРНЕТА
    #mixes = dict()
    mixes = list()
    #for i in range(1, 800):
    for i in range(1,40):
        try:
            #mix_str = "mixes/"
            html = urllib.request.urlopen(url_mixes + str(i) + '/versions')

            #print(html.read())
            page_soup = soup(html, 'html.parser')

            parsed = page_soup.find('a', {'href':'/mixes/' + str(i)})

            nameMix = chng_mix(parsed.text)
            year = [parsed.text.split()[len(parsed.text.split()) - 2][:-1],
                        parsed.text.split()[len(parsed.text.split()) - 1]]

            versions = list()
            if nameMix:
                print(nameMix)
                #print(page_soup.find_all('div', {'class':'media-body'}).text)
                parsed = page_soup.find_all('a', {'class':'list-group-item'})
                #songs.append(parsed.text.split())
                for j in range(len(parsed)):
                    print(parsed[j].text.split()[0])
                    versions.append(parsed[j].text.split()[0])

                versions.sort()
                #print(parsed.text.split()[len(parsed.text.split()) - 2])
                #mixes[nameMimix_dict = dict()x] = {"versions": versions, "year": year}
                mixes.append({'name': nameMix, "versions": versions, "data ": year})
                #print([nameMix, {"versions": versions, "year": year}])
                print()

        except urllib.error.HTTPError:
            logging.warning("HttpError")
        except Exception as e:
            logging.error(e)

    for mix in mixes:
        print(mix)

    return mixes


if __name__ == '__main__':
    convertSongs(50)

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
