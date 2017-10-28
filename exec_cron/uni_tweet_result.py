import sys, os

# 一個上の階層ディレクトリをライブラリパスとして追加
here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(here,".."))
import twitter as twitter

sys.path.append(os.path.join(here, "..", "auth_file"))
import uniauth


tw = twitter.Twitter()
tw.tweet_playlog(uniauth.ID, uniauth.PASS)

