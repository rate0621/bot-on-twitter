from requests_oauthlib import OAuth1Session
from pytz import timezone
from datetime import datetime, timedelta
from time import sleep
import pytz
import json
import authkey
import re
import uni_common_tools.ChunithmNet as ChunithmNet
from pprint import pprint


import sys

import lib.PrepareChain as PrepareChain
import lib.GenerateText as GenerateText

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

  def tweet_playlog(self):
    """
    現在時刻から、1時間以内にプレイしたリザルトをツイッターに呟く
    @param なし
    @return なし
    """
    args = sys.argv
    cn = ChunithmNet.ChunithmNet(args[1], args[2])
    #play_logs = cn.get_playlog_detail()

    now = datetime.now()
    hour = timedelta(hours=6)
    since = now - hour

    ## datetime.nowで得られた日付を[yyyy-mm-dd HH:MM]の形式にするためいったん文字列にする
    now = now.strftime('%Y-%m-%d %H:%M')
    since = since.strftime('%Y-%m-%d %H:%M')

    ## 比較するためもう一度日付型に戻す
    now = datetime.strptime(now, '%Y-%m-%d %H:%M')
    since = datetime.strptime(since, '%Y-%m-%d %H:%M')

    num = 0
    while 1:
      play_log = cn.get_playlog_detail(num)

      # プレイした時間が、1時間以内かをチェック。もし範囲外ならその時点でループを抜ける
      play_date = play_log["play_date"]
      play_date = datetime.strptime(play_date, '%Y-%m-%d %H:%M')
      if since < play_date < now:
        send_text = "【チュウニズム リザルト】\nプレイ日時:" + play_log["play_date"] + "\n曲名:" + play_log["music_title"] + "\nMAX COMBO:" + play_log["max_combo"] + "\nScore:" + play_log["score"] + "\nJC:" + play_log["justice_critical"] + "\nJ:" + play_log["justice"] + "\nAttack:" + play_log["attack"] + "\nMiss:" + play_log["miss"]
        self.post_tweet(send_text)
        print (send_text)
        sleep (5)
        num = num + 1
        continue
      else:
        print ("時間範囲外のためループを抜ける")
        break



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
    tweet_list = json.loads(res.text)

    return tweet_list


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
      "count": "200"
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
      # https://api.twitter.com/1.1/search/tweets.jsonから取得したときのループ
      if 'statuses' in tweet_list:
        for tweet in tweet_list["statuses"]:
          tweet_text = tweet["text"]
          tweet_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet_text)  # http(s)的な文字列の削除
          tweet_text = re.sub(r'@\w+', "", tweet_text) # 「@hogehoge 今日暇？」 を、「今日暇？」に書き換え

          f.write(tweet_text)
          f.flush()

      # https://api.twitter.com/1.1/statuses/user_timeline.jsonから取得したときのループ
      else:
        for tweet in tweet_list:
          tweet_text = tweet["text"]
          tweet_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet_text)  # http(s)的な文字列の削除
          tweet_text = re.sub(r'@\w+', "", tweet_text) # 「@hogehoge 今日暇？」 を、「今日暇？」に書き換え

          f.write(tweet_text)
          f.flush()
    
    return file_name

  def stream(self):
    """
    いったん以下のコードで自分の呟きをリアルタイムで取得できる
    受け取ったテキストによって色々処理をわけたりできそうで夢が広がるけどいったん保留
    """
    url = "https://stream.twitter.com/1.1/statuses/filter.json"
    #res = self.twitter.post(url, stream=True, data={"follow":"chatrate"})
    res = self.twitter.post(url, stream=True, data={"follow":"521317771"})

    for line in res.iter_lines():
      if line:
        decode_line = json.loads(line.decode("utf-8"))
        print (decode_line["text"])


if __name__ == '__main__':
  tw = twitt()

  ### ツイッターからツイートを拾ってきてマルコフ連鎖とかする
  #tweet_list = tw.get_tweet_including_words("チュウニズム")
  #tweet_list = tweet_list = tw.get_tweet_specific_user("chatrate")
  #file_name = tw.output_to_file(tweet_list)
  #chain = PrepareChain.PrepareChain(file_name)
  #triplet_freqs = chain.make_triplet_freqs()
  #chain.save(triplet_freqs, True)
  #generator = GenerateText.GenerateText(2)
  #gen_text = generator.generate()
  #tw.post_tweet(gen_text + "【このツイートは自動生成されたものです】")

  #tw.get_home_timeline()

  ### ウニのプレイログを呟く
  tw.tweet_playlog()


  ### ストリーミング
  #tw.stream()
