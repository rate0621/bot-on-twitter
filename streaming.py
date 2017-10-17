from requests_oauthlib import OAuth1Session
import json
import authkey
import re
import uni_common_tools.ChunithmNet as ChunithmNet
from pprint import pprint

import sys

import lib.PrepareChain as PrepareChain
import lib.GenerateText as GenerateText

import twitter as twitter

tw = twitter.twitt()

user_id = []
user_id.append(tw.get_userid_from_screen_name("chatrate"))

for item in tw.streaming(follow=user_id):
  print (item["text"])
