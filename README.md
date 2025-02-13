# Vector Database Sample

このプロジェクトは、Milvus ベクトルデータベースを使用した基本的な操作のサンプルコードです。

## 環境構築

### 前提条件

- Docker
- Docker Compose

### 実行手順

1. リポジトリをクローンまたはダウンロード

```bash
git clone <repository-url>
cd sample-vector-database
```

2. Docker コンテナのビルドと起動

```bash
docker compose up --build -d
```

すべてのコンテナ（python、milvus-standalone、milvus-etcd、milvus-minio）が起動し、自動的にサンプルコードが実行されます。

## ログの確認

Python コンテナのログを確認するには：

```bash
docker compose logs python
```

このサンプルコードは以下の操作を実行します：

1. Milvus サーバーへの接続
2. コレクションの作成
3. ランダムなベクトルデータの生成と挿入
4. ベクトル類似度検索の実行

## コンテナの停止

使用が終わったら、以下のコマンドでコンテナを停止できます：

```bash
docker compose down
```

## 注意事項

- デフォルトでは、データは`./volumes`ディレクトリに保存されます
- このサンプルは開発環境用の設定です。本番環境での使用には適切なセキュリティ設定が必要です
