from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
import numpy as np


# Milvusサーバーに接続
def connect_to_milvus():
    connections.connect(host='standalone', port='19530')
    print("Connected to Milvus server")


# コレクションの作成
def create_collection(collection_name, dim):
    if utility.has_collection(collection_name):
        utility.drop_collection(collection_name)

    # フィールドの定義
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64,
                    is_primary=True, auto_id=True),
        FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
        FieldSchema(name="color", dtype=DataType.VARCHAR, max_length=10)
    ]

    schema = CollectionSchema(
        fields=fields, description="Sample collection for vector similarity search")
    collection = Collection(name=collection_name, schema=schema)

    # インデックスパラメータの設定
    index_params = {
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }

    # ベクトルフィールドにインデックスを作成
    collection.create_index(field_name="vector", index_params=index_params)
    print(f"Collection {collection_name} created successfully")
    return collection


# データの挿入
def insert_data(collection, num_entities=3000):
    # ランダムなベクトルデータを生成
    dim = 128
    vectors = np.random.rand(num_entities, dim).astype(np.float32)
    colors = np.random.choice(['red', 'green', 'blue'], size=num_entities)

    # データを挿入
    entities = [
        vectors.tolist(),
        colors.tolist()
    ]

    collection.insert(entities)
    collection.flush()
    print(f"Inserted {num_entities} entities")


# ベクトル検索の実行
def search_vectors(collection, search_vectors, top_k=5):
    collection.load()

    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10}
    }

    results = collection.search(
        data=search_vectors,
        anns_field="vector",
        param=search_params,
        limit=top_k,
        output_fields=["color"]
    )

    return results


def main():
    # Milvusに接続
    connect_to_milvus()

    # コレクションを作成
    collection_name = "example_collection"
    dim = 128
    collection = create_collection(collection_name, dim)

    # データを挿入
    insert_data(collection)

    # 検索用のクエリベクトルを生成
    query_vector = np.random.rand(1, dim).astype(np.float32)

    # 検索を実行
    results = search_vectors(collection, query_vector.tolist())

    # 結果を表示
    for i, hits in enumerate(results):
        print(f"\nSearch result for query vector {i}:")
        for hit in hits:
            print(
                f"ID: {hit.id}, Distance: {hit.distance}, Color: {hit.entity.get('color')}")


if __name__ == "__main__":
    main()
