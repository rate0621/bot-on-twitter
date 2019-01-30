# Text Generator
マルコフ連鎖を使った文章自動生成プログラム

## 元ネタ
https://github.com/karaage0703/TextGenerator
上記リポジトリのものをほぼそのまま流用（一部Mecab本体(?)にバグがあり正常に動かない箇所を手直ししてる）

## 使い方
`python PrepareChain.py sample.txt`

`sample.txt` は元ネタとなる文章が記載されたファイル

すると、
`chain.db`
というdbファイルが出来上がるので


`python GenerateText.py 3`
で文章が生成される。

