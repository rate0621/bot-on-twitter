from requests_oauthlib import OAuth1Session
import json
import authkey

class twitt():
  def __init__():
    # 今はファイルから読み込んでいるけどデプロイするときはherokuの環境変数に入れる
    self.twitter = OAuth1Session(authkey.CONSUMER_KEY, authkey.CONSUMER_SECRET, authkey.ACCESS_TOKEN, authkey.ACCESS_TOKEN_SECRET)

  def get_home_timeline():
    params = {}
    req = self.twitter.get("https://api.twitter.com/1.1/statuses/home_timeline.json", params = params)

    timeline = json.loads(req.text)

    for tweet in timeline:
      print (tweet["text"])
