import sys, os, re

here = os.path.join( os.path.dirname(os.path.abspath(__file__)))

class Libs():
    def __init__(self):
        pass


    def output_to_file(self, tweet_list):

        file_name = here + "/common_lib/tweet.txt"

        with open(file_name, "w") as f:
            # https://api.twitter.com/1.1/search/tweets.jsonから取得したときのループ
            if 'statuses' in tweet_list:
                for tweet in tweet_list["statuses"]:
                    tweet_text = tweet["text"]
                    tweet_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet_text)  # http(s)的な文字列の削除
                    tweet_text = re.sub(r'@\w+', "", tweet_text) # 「@hogehoge 今日暇？」 を、「今日暇？」に書き換え
                    tweet_text = re.sub(r'#\w+', "", tweet_text) # 「#hogehoge 今日暇？」 を、「今日暇？」に書き換え

                    f.write(tweet_text)
                    f.flush()

            # https://api.twitter.com/1.1/statuses/user_timeline.jsonから取得したときのループ
            else:
                for tweet in tweet_list:
                    tweet_text = tweet["text"]
                    tweet_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", tweet_text)  # http(s)的な文字列の削除
                    tweet_text = re.sub(r'@\w+', "", tweet_text) # 「@hogehoge 今日暇？」 を、「今日暇？」に書き換え
                    tweet_text = re.sub(r'#\w+', "", tweet_text) # 「#hogehoge 今日暇？」 を、「今日暇？」に書き換え

                    f.write(tweet_text)
                    f.flush()

        return file_name
