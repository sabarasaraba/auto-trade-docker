# auto-trade-docker

マイニングで得た ETH を自動で BETH にするシステムを作るよ。
ゆくゆくは LINE Bot 通知とかも実装するよ

## 環境構築方法

前提条件：docker が使える環境であること。

1. 本リポジトリを clone してローカルに持ってくる
2. BinanceAPI キー・BinancePool におけるマイニングユーザー名を自身のアカウントから取得し、プロジェクトフォルダ直下に.env ファイルとして下記のように作成

```
API_KEY = '自身のAPIキーを記載'
API_SECRET = '自身のAPIシークレットキーを記載'
MINING_ALGOLISM = 'ETHの場合、ethash BTCの場合、sha256'
MINING_USER_NAME = 'バイナンスプールでのマイニングユーザー名'
LINE_CHANNEL_ACCESS_TOKEN = '通知用LineBotのチャンネルアクセストークン'
LINE_USER_ID = 'PUSH通知を送るLineアカウントのユーザーID'
```

3. プロジェクトフォルダ直下(Dockerfile がある場所)で以下コマンドを実行

```
docker-compose up -d --build
```

4. 以下コマンドで Python スクリプトを実行

```
docker-compose exec app python src/main.py
```

## 更新反映方法

1. git pull で最新ソースコードを取得

```
git pull origin master
```

2. DockerFile 更新内容反映のためイメージ・コンテナの再作成

```
docker-compose down
docker-compose build
docker-compose up -d
```

## Python モジュール新規追加時反映方法(開発環境で以下を実施後は上の「更新反映方法」を実施すること)

1. 開発環境ホストマシン上で欲しいモジュールを poetry add で追加する(以下は line-bot-sdk 追加時の例)

```
poetry add line-bot-sdk
```

2. 新しいイメージを作成し、コンテナを生成する

```
docker-compose up -d --build
```

## 導入済み Python モジュールのバージョンアップ方法(開発環境で以下を実施後は上の「更新反映方法」を実施すること)

1. pyproject.toml 内でアップデートしたいモジュールのバージョンをアップデートバージョンに変更する形で編集する

2. アップデートしたいモジュールのアップデートを実行

```
poetry update <モジュール名>
```

## 参考文献

これで Docker 環境のイメージは掴んだよ

- https://qiita.com/reflet/items/4b3f91661a54ec70a7dc

掴んだところで poetry で混ぜ込む方法はこっちを参考にしたよ

- https://qiita.com/Aruneko/items/43efd6d7aa8eccc2b77e

python-binance のトレードでの具体的な使い方とかはこれを参考にしたよ

- https://dot-blog.jp/news/binance-api-beginners-haw-to/

BinanceAPI を Postman で呼び出す方法はこれがとてもいいよ。

- https://academy.binance.com/ja/articles/binance-api-series-pt-1-spot-trading-with-postman

Windows での実行用に Docker インストールする際にはこの公式ページを参考にしたよ。

- https://docs.docker.jp/docker-for-windows/install-windows-home.html

Poetry 管理モジュールのアップデート方法はこのページを参考にしたよ

- https://qiita.com/canonrock16/items/f77ee2a2df9be5b8cc37
