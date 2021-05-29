# auto-trade-docker

マイニングで得た ETH を自動で BETH にするシステムを作るよ。
ゆくゆくは LINE Bot 通知とかも実装するよ

## 環境構築方法

前提条件：docker が使える環境であること。

1. 本リポジトリを clone してローカルに持ってくる
2. プロジェクトフォルダ直下(Dockerfile がある場所)で以下コマンドを実行

```
docker-compose up -d --build
```

3. 以下コマンドで Python スクリプトを実行

```
docker-compose exec app python src/main.py
```

## 参考文献

これで Docker 環境のイメージは掴んだよ

- https://qiita.com/reflet/items/4b3f91661a54ec70a7dc

掴んだところで poetry で混ぜ込む方法はこっちを参考にしたよ

- https://qiita.com/Aruneko/items/43efd6d7aa8eccc2b77e
