import sys, os
from datetime import datetime, timedelta
from time import sleep

# 一個上の階層ディレクトリをライブラリパスとして追加
here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(here,".."))
import twitter as twitter
import common_lib.uni_common_tools.ChunithmNet as ChunithmNet

sys.path.append(os.path.join(here, "..", "auth_file"))
import uniauth


now = datetime.now()
past = timedelta(minutes=30)
since = now - past

## datetime.nowで得られた日付を[yyyy-mm-dd HH:MM]の形式にするためいったん文字列にする
now = now.strftime('%Y-%m-%d %H:%M')
since = since.strftime('%Y-%m-%d %H:%M')

## 比較するためもう一度日付型に戻す
now = datetime.strptime(now, '%Y-%m-%d %H:%M')
since = datetime.strptime(since, '%Y-%m-%d %H:%M')

cn = ChunithmNet.ChunithmNet(uniauth.ID, uniauth.PASS)
tw = twitter.Twitter()
num = 0

while 1:
  play_log = cn.get_playlog_detail(num)

  # プレイした時間が、1時間以内かをチェック。もし範囲外ならその時点でループを抜ける
  play_date = play_log["play_date"]
  play_date = datetime.strptime(play_date, '%Y-%m-%d %H:%M')
  if since < play_date < now:
    send_text = \
"【チュウニズム リザルト】\n\
PlayDate     ：" + play_log["play_date"] + "\n\
Music          ：" + play_log["music_title"] + "\n\
MaxCombo ：" + play_log["max_combo"] + "\n\
Score          ：" + play_log["score"] + "\n\
JC               ：" + play_log["justice_critical"] + "\n\
J              　：" + play_log["justice"] + "\n\
Attack　　  ：" + play_log["attack"] + "\n\
Miss            ：" + play_log["miss"]

    tw.post_tweet(send_text)
    print (send_text)
    sleep (120)
    num = num + 1
    continue
  else:
    print ("時間範囲外のためループを抜ける")
    break

