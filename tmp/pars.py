import bs4
from bs4 import BeautifulSoup as soup #parses/cuts  the html

import traceback
import urllib.request

def chng_str(txt):
    pre_res = txt.split()
    if "Arcade" not in pre_res:
        return ""
        
    res = ""
    for word in pre_res:
        if word == "ID:":
            break
        res += word + ' '
    
    return res

fiesta_url = "https://pumpout.anyhowstep.com/search/results?display=song&song_version=1~23&page="
prime_url = "https://pumpout.anyhowstep.com/search/results?display=song&song_version=1~125&page="
prime2_url = "https://pumpout.anyhowstep.com/search/results?display=song&song_version=1~143&page="
xx_url = "https://pumpout.anyhowstep.com/search/results?display=song&song_version=1~146&page="

#list of links
url_list = [fiesta_url, prime_url, prime2_url, xx_url]

#lists of songs
song_list = [[] for c in range(4)]

for i in range(len(url_list)):
    url = url_list[i]

    for j in range(1,25):
        try:
            html = urllib.request.urlopen(url+str(j)).read()
            #div class="media-body"
            page_soup = soup(html, "html.parser")

            res_list = page_soup.find_all('div', {'class':'media-body'})

            for res in res_list:
                song = chng_str(res.text)
                if(song):
                    #print(song)
                    song_list[i].append(song)
                
            #print(page_soup.find('div', {'class':'media-body'}).text)
            
        except Exception:
            print('Ошибка:\n', traceback.format_exc())

#print(song_list)

#for i in range(len(song_list)):
#    print(song_list[i])


RESULT = list()

for song in song_list[3]:
    if song in song_list[0] and\
       song in song_list[1] and\
       song in song_list[2] and\
       song in song_list[3]:
        RESULT.append(song)

for song in RESULT:
    print(song)

'''
my_url = 'http://www.fortwiki.com/Battery_Adair'
print(my_url)
uClient = uReq(my_url) #opens the HTML and stores it in uClients

page_html = uClient.read() # reads the URL
uClient.close() # closes the URL

page_soup = soup(page_html, "html.parser") #parses/cuts the HTML
containers = page_soup.find_all("table")
'''
