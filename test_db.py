import dataset

# データベースに接続する
db = dataset.connect("sqlite:///db/test.db")

# テーブル内のデータを全削除
db["users"].delete()
table = db["users"]

# データ挿入
table.insert({"name": "test1", "age": 1})
table.insert({"name": "test2", "age": 2})

all_data = [dict(row) for row in table.all()]

print(all_data)