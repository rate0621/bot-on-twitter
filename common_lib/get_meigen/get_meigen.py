import urllib.request
from urllib.parse import urlencode
import sys, os
import random
import re
import codecs
from bs4 import BeautifulSoup

here = os.path.join( os.path.dirname(os.path.abspath(__file__)))

url = "http://www.iwako-light.com/entry/diary/post-3196/"

req = urllib.request.Request(url, None)
with urllib.request.urlopen(req) as res:
  html = res.read().decode("utf-8")
  res.close()


soup = BeautifulSoup(html, "html.parser")
hoge = soup.find_all("blockquote")

file_path = here + "/../../data/meigen.text"
for i in hoge:
  with codecs.open(file_path, "a", "utf-8") as f:
    f.write(re.sub("[「|」]", "", i.text) + "\n")
    f.flush()



