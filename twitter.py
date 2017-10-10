from requests_oauthlib import OAuth1Session
import json
import authkey
import uni_common_tools.ChunithmNet as ChunithmNet

import sys

import lib.PrepareChain as PrepareChain

class twitt():
  def __init__(self):
    # 今はファイルから読み込んでいるけどデプロイするときはherokuの環境変数に入れる
    self.twitter = OAuth1Session(authkey.CONSUMER_KEY, authkey.CONSUMER_SECRET, authkey.ACCESS_TOKEN, authkey.ACCESS_TOKEN_SECRET)
    

  def get_home_timeline(self):
    params = {}
    res = self.twitter.get("https://api.twitter.com/1.1/statuses/home_timeline.json", params = params)

    timeline = json.loads(res.text)

    for tweet in timeline:
      print (tweet["text"])

  def tweet_last_playlog(self):
    cn = ChunithmNet.ChunithmNet("", "")
    play_logs = cn.get_playlog()
    send_text = ""
    for play_log in play_logs:
      send_text = "【チュウニズム リザルト自動呟くマン】\nプレイ日時:" + play_log["play_date"] + "\n楽曲名:" + play_log["music_name"] + "\nスコア:" + play_log["score"]

      #print (play_log["track_number"])
      #print (play_log["play_date"] + "に")
      #print (play_log["music_name"] + "をプレイした結果")
      #print (play_log["score"] + "でした")
      break

    self.post_tweet(send_text)

  def post_tweet(self, text):
    params = {"status": text}
    res = self.twitter.post("https://api.twitter.com/1.1/statuses/update.json", params=params)
    print (res)

  def get_tweet_including_words(self, search_word):
    '''
    引数で渡した単語を含むツイートを検索し、
    tweet.txtに吐き出す。
    '''

    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
      #"q": unicode(search_words, "utf-8"),
      "q": search_word.encode("utf-8"),
      "lang": "ja",
      "result_type": "recent",
      "count": "100"
    }

    res = self.twitter.get(url, params = params)
    tweets = json.loads(res.text)
    with open("lib/tweet.txt", "w") as f:
      for tweet in tweets["statuses"]:
        tweet_text = (tweet["text"])
        if "http" in tweet_text:
          tweet_text = tweet_text.split("http", 1)[0]
          tweet_text = tweet_text.split("@")[0]
          tweet_text = tweet_text.split("RT")[0]

        f.write(tweet_text)
        f.flush()

    pc = PrepareChain.PrepareChain("tweet.txt")
    triplet_freqs = pc.make_triplet_freqs()
    pc.save(triplet_freqs, True)


if __name__ == '__main__':
  tw = twitt()
  tw.get_tweet_including_words("チュウニズム")
  #tw.get_home_timeline()
  #tw.tweet_last_playlog()
  #tw.post_tweet("this is test")
