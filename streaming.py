from requests_oauthlib import OAuth1Session
import json
import authkey
import re
from pprint import pprint

import sys

import common_lib.uni_common_tools.ChunithmNet as ChunithmNet
import common_lib.markov.PrepareChain as PrepareChain
import common_lib.markov.GenerateText as GenerateText

# ここでimportしているのは公式謹製のものではなく、自分で作ったtwitterライブラリ
import twitter as twitter

tw = twitter.twitt()

user_id = []
user_id.append(tw.get_userid_from_screen_name("chatrate"))

for item in tw.streaming(follow=user_id):
  print (item["text"])
