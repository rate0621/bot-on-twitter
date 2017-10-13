from requests_oauthlib import OAuth1Session
from pytz import timezone
from datetime import datetime
import json
import authkey
import re
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

    args = sys.argv
    cn = ChunithmNet.ChunithmNet(args[1], args[2])
    play_logs = cn.get_playlog()
    send_text = ""
    play_date = ""
    for play_log in play_logs:
      #send_text = "【チュウニズム リザルト自動呟くマン】\nプレイ日時:" + play_log["play_date"] + "\n楽曲名:" + play_log["music_name"] + "\nスコア:" + play_log["score"]

      play_date = play_log["play_date"]
      print (play_date)
      break

    now_date = datetime.now(timezone('Asia/Tokyo')).strftime("%Y/%m/%d %H:%M:%S")
    print (play_date)
    print (now_date)
    #self.post_tweet(send_text)

  def post_tweet(self, text):
    params = {"status": text}
    res = self.twitter.post("https://api.twitter.com/1.1/statuses/update.json", params=params)
    print (res)

  def get_tweet_including_words(self, search_word):
    '''
    引数で渡した単語を含むツイートを取得する
    @param search_word(string)
    @return tweet_list(json)
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

    pc = PrepareChain.PrepareChain("lib/tweet.txt")
    triplet_freqs = pc.make_triplet_freqs()
    pc.save(triplet_freqs, True)

  def get_tweet_specific_user(self, screen_name):
    """
    特定ユーザのツイートを取得する
    @param  screen_name(string)
    @return tweet_list(json)
    """

    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
      #"q": unicode(search_words, "utf-8"),
      "screen_name": screen_name.encode("utf-8"),
      "include_rts": "false",
      "exclude_replies": "false",
      "count": "100"
    }

    res = self.twitter.get(url, params = params)
    tweet_list = json.loads(res.text)

    return tweet_list

  def output_to_file(self, tweet_list):
    """
    get_tweet_specific_userやget_tweet_including_wordsなどから返ってきたtweet_listをテキストファイルに出力
    @param tweet_list(json)
    @return file_name(string)
    """

    file_name = "lib/tweet.txt"

    with open(file_name, "w") as f:
      for tweet in tweet_list:
        tweet_text = tweet["text"]
        tweet_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet_text)  # http(s)的な文字列の削除
        tweet_text = re.sub(r'@\w+', "", tweet_text) # 「@hogehoge 今日暇？」 を、「今日暇？」に書き換え

        f.write(tweet_text)
        f.flush()
    
    return file_name

if __name__ == '__main__':
  tw = twitt()
  #tw.get_tweet_including_words("リーダブルコード")
  tweet_list = tw.get_tweet_specific_user("chatrate")
  file_name = tw.output_to_file(tweet_list)
  #tw.get_tweet_including_words("リーダブルコード")
  #tw.get_home_timeline()
  #tw.tweet_last_playlog()
  #tw.post_tweet("this is test")
