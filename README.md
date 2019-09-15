# benefit_sukusuku
このソフトは、benefit stationのすくすくmonthlyのサービスを利用する際のログインからフォームへの入力を自動化するプログラムです。
毎月、同じような入力を入れるのが面倒なので作ってみました。
主な特徴は下記の通り
- ログインからフォームのほぼすべての内容の記入が自動化
- 記入内容は設定ファイル(YAML形式)から取り込む
- アップロードすべきファイルを事前にディレクトリに格納しておけば自動でアップロード

# Dependency
- python3.7の実行環境が必要です。
- pythonの各種パッケージについてはrequirement.txtを参照下さい

# Setup
本ソフトはPythonスクリプトであるため、pythonの実行環境が必要です。
また、ブラウザを制御するため、chromedriverを事前にインストールしておく必要があります。
- chromedriverのインストール
    - brew install chromedriver
- Pythonのパッケージをインストール
    - pip install -r requirements.txt

# Usage
- 使い方
    - 設定ファイル(YAML形式)を作成する。(サンプルのparameters_sample.yamlを参照してください。)
    - python autofill.py <設定ファイルのパス名>
- サンプルコード
    python autofill.py sampledata/parameters_sample.yaml 

# License
This software is released under the MIT License, see LICENSE.

# Authors
このリポジトリ内のすべてのコードは、jun-s-19が作成しました。

# References
参考にした情報源（サイト・論文）などの情報、リンク

- Selenium ChromeDriver & PythonをMacで動かす準備メモ
    https://qiita.com/y__ueda/items/7b6f2a95ea45667e1029

- すくすくmonthly
    https://bs.benefit-one.co.jp/bs/pages/bs/srch/menuPrticSrchRslt.faces?menuNo=642245