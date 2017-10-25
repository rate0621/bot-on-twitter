import sys, os

# 一個上の階層ディレクトリをライブラリパスとして追加
here = os.path.join( os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(here,".."))

import twitter as twitter
import lib.markov.PrepareChain as PrepareChain
import lib.markov.GenerateText as GenerateText

meigen_file = here + "/../data/meigen.text"

chain = PrepareChain.PrepareChain(meigen_file)
triplet_freqs = chain.make_triplet_freqs()
chain.save(triplet_freqs, True)
generator = GenerateText.GenerateText(5)
gen_text = generator.generate()

tw = twitter.Twitter()
tw.post_tweet(gen_text)

