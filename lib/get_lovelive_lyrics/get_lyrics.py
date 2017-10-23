import urllib.request
from urllib.parse import urlencode
import sys, os
import random
import re
import codecs
from bs4 import BeautifulSoup

class getLyrics:
  def get_music_link_list(self):
    uta_net_url = "https://www.uta-net.com/artist/10739/"

    req = urllib.request.Request(uta_net_url, None)
    with urllib.request.urlopen(req) as res:
      html = res.read().decode("utf-8")
      res.close()

    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all(class_="side td1")

    link_list = []
    for article in articles:
      link_list.append(article.a.get('href'))

    return link_list

  def get_lyrics(self, link_list):
    base_url = "https://www.uta-net.com/"
    link = random.choice(link_list)
    lyric_url = base_url + link


    req = urllib.request.Request(lyric_url, None)
    with urllib.request.urlopen(req) as res:
      html = res.read().decode("utf-8")
      res.close()

    soup = BeautifulSoup(html, "html.parser")
    article = soup.find(id="kashi_area")

    lyric = re.sub('<br(\/)?>','\n', str(article))
    lyric = re.sub("<.*?>","", lyric)

    #print (lyric)

    file_name = "../lyric.text"
    with codecs.open(file_name, "a", "utf-8") as f:
    #with open(file_name, "w") as f:
      f.write(lyric)
      f.flush()
      

######


gl = getLyrics()
link_list = gl.get_music_link_list()
gl.get_lyrics(link_list)
