---
name: mongodb-query
type: tool
module: tools
status: verified
confidence: 0.8
created: 2026-04-16
last_validated: 2026-04-16
tags: [mongodb, pymongo, query, database]
---

# MongoDB 查询工具参考

## 连接方式

使用 pymongo（mongosh 不兼容旧版 MongoDB 3.4，详见 [[mongosh-wire-version|pitfalls/tools/mongosh-wire-version]]）

```python
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime, date

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client['dbname']
```

## BSON 序列化

pymongo 返回的文档包含 BSON 特有类型，必须用自定义 JSON 编码器处理 ObjectId 和 datetime，否则 `json.dumps` 会报 TypeError。

## 常用查询模式

```python
# 按字段查询
results = db.collection.find({'field': 'value'})

# 按 ObjectId 查询
results = db.collection.find({'_id': ObjectId('...')})

# 计数
count = db.collection.count_documents({'field': 'value'})

# 列出所有集合
colls = db.list_collection_names()
```

## 相关条目

- [[mongosh-wire-version|pitfalls/tools/mongosh-wire-version]]
