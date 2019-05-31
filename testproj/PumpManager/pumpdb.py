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


def getSong(i):
    logging.basicConfig(filename='history.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)

    url_songs = "https://pumpout.anyhowstep.com/songs/"

    #ПОФИКСИТЬ ЕСЛИ НЕТ ИНТЕРНЕТА
    res = dict()

    res['charts'] = list()
    res['mixes'] = list()
    #for i in range(1, 800):

    try:
        html = urllib.request.urlopen(url_songs + str(i))
        #print(html.read())
        page_soup = soup(html, 'html.parser')
        #print(page_soup.find_all('div', {'class':'media-body'}).text)
        parsed = page_soup.find('div', {'class':'media-body'})
        res['songs'] = parsed.text.split()
        #print(songs[len(songs)-1])

        parsed = page_soup.find_all('img', {'class':'thumb pull-left'})
        #print(parsed)

        for pars in parsed:
            res['charts'].append(
            {'lvl' : pars['src'][15:][:-4][-2:],
            'type':  re.search("/\w{1,4}/", pars['src']).group()[1:-1]})

        parsed = page_soup.find_all('a', {'class': "accordian-toggle"})
        for pars in parsed:
            res['mixes'].append(' '.join(pars.text.split()))

        parsed = page_soup.find_all('span', {'class':"label bg-primary", 'href' : ''})

        print(res)
        song_dict = res
        song_lst, charts, mixes = song_dict['songs'], song_dict['charts'], song_dict['mixes']

        song = dict()
        song['name'] = []

        song['charts'] = charts
        song['mixes'] = mixes
        for j in range(len(song_lst)):
            if song_lst[j] != "ID:":
                song['name'].append(song_lst[j])
            else:
                song['name'] = ' '.join(song['name'])
                for k in range(j+2,len(song_lst)):
                    if song_lst[k] == "BPM":#.isdigit() or re.search("/\d{1,3}.?\d{0,3}/", pars['src']).group()[1:-1]:
                        #song['author'] = []
                        #for l in range(k-j-3):
                        #    song['author'].append(song_lst[j+2+l])
                        #song['author'] = ' '.join(song['author'])
                        song['bpm'] = song_lst[k-1]
                        if song_lst[k+1] == 'Full' or song_lst[k+1] == 'Short':
                            song['type'] = song_lst[k+1] + ' ' + song_lst[k+2]
                            song['cathegory'] = song_lst[k+3]
                        else:
                            song['type'] = song_lst[k+1]
                            song['cathegory'] = song_lst[k+2]

                break
        song['author'] = []
        for i in range(len(parsed)):
            if not i or parsed[i].text != parsed[i].text.upper():
                song['author'].append(parsed[i].text)
        song['author'] = ', '.join(song['author'])

        if song['type'] == "Short Cut":
            song['name'] = song['name'] + '/Short Cut'
        elif song['type'] == "Full Song":
            song['name'] = song['name'] + '/Full Song'

        return song

    except urllib.error.HTTPError:
        logging.warning("HttpError")
    except Exception as e:
        logging.error(e)

    return None


def convertSongs(q):
    song_dict = getSong(q)
    song_lst, charts, mixes = song_dict['songs'], song_dict['charts'], song_dict['mixes']

    song = dict()
    song['name'] = []

    song['charts'] = charts
    song['mixes'] = mixes
    for j in range(len(song_lst)):
        if song_lst[j] != "ID:":
            song['name'].append(song_lst[j])
        else:
            song['name'] = ' '.join(song['name'])
            for k in range(j+2,len(song_lst)):
                if song_lst[k] == "BPM":#.isdigit() or re.search("/\d{1,3}.?\d{0,3}/", pars['src']).group()[1:-1]:
                    song['author'] = []
                    for l in range(k-j-3):
                        song['author'].append(song_lst[j+2+l])
                    song['author'] = ' '.join(song['author'])
                    song['bpm'] = song_lst[k-1]
                    if song_lst[k+1] == 'Full' or song_lst[k+1] == 'Short':
                        song['type'] = song_lst[k+1] + ' ' + song_lst[k+2]
                        song['cathegory'] = song_lst[k+3]
                    else:
                        song['type'] = song_lst[k+1]
                        song['cathegory'] = song_lst[k+2]

            break


    if song['type'] == "Short Cut":
        song['name'] = song['name'] + '/Short Cut'
    elif song['type'] == "Full Song":
        song['name'] = song['name'] + '/Full Song'

    return song

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
