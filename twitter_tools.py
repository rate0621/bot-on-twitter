import sys, os


here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(here)

from twitter import Twitter
import libs as Libs
import common_lib.markov.PrepareChain as PrepareChain
import common_lib.markov.GenerateText as GenerateText




class TwitterTools(Twitter):
    def __init__(self):
        super().__init__()

    def tweet_markov_from_specific_user(self, screen_name):
        """
        渡されたscreen_name（@ユーザ名）の過去のツイートを取得してマルコフ連鎖を用いて文章を生成して呟く
        @param  screen_name(string)
        @return なし
        """
        tweet_list = self.get_tweet_specific_user(screen_name)
        libs = Libs.Libs()
        file_name = libs.output_to_file(tweet_list)
        chain = PrepareChain.PrepareChain(file_name)
        triplet_freqs = chain.make_triplet_freqs()
        chain.save(triplet_freqs, True)
        generator = GenerateText.GenerateText(3)
        gen_text = generator.generate()
        #tw.post_tweet(gen_text + "【このツイートは自動生成されたものです】")
        return gen_text


    def tweet_markov_from_specific_word(self, search_word):
        """
        渡されたsearch_word（検索文字列）を含むツイートを取得してマルコフ連鎖を用いて文章を生成して呟く
        @param  search_word(string)
        @return なし
        """
        tweet_list = self.get_tweet_including_words(search_word)
        libs = Libs.Libs()
        file_name = libs.output_to_file(tweet_list)
        chain = PrepareChain.PrepareChain(file_name)
        triplet_freqs = chain.make_triplet_freqs()
        chain.save(triplet_freqs, True)
        generator = GenerateText.GenerateText(4)
        gen_text = generator.generate()
        #tw.post_tweet(gen_text + "【このツイートは自動生成されたものです】")
        print (gen_text + "【このツイートは自動生成されたものです】")


if __name__ == '__main__':
    tt = TwitterTools()
    tt.tweet_markov_from_specific_user('puriconemaru')
