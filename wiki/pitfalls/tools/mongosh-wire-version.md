---
name: mongosh-wire-version
type: pitfall
module: tools
status: verified
confidence: 0.9
created: 2026-04-16
last_validated: 2026-04-16
tags: [mongodb, mongosh, pymongo, wire-version, compatibility]
---

# mongosh 与旧版 MongoDB 不兼容

## 问题描述

使用 `mongosh`（2.8.2）连接 MongoDB 3.4 副本集时报错：

```
MongoServerSelectionError: Server at mongo1:27017 reports maximum wire version 4,
but this version of the Node.js Driver requires at least 8 (MongoDB 4.2)
```

mongosh 内置的 Node.js Driver 要求 MongoDB >= 4.2（wire version >= 8），而旧版 MongoDB 3.4（wire version 4）不满足。

## 解决方案

使用 Python `pymongo` 替代 mongosh 连接旧版 MongoDB：

```python
from pymongo import MongoClient
client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
db = client['dbname']
for doc in db.collection.find():
    print(doc)
```

## 要点

- mongosh 与 MongoDB 服务器版本有最低兼容要求，不向下兼容
- pymongo 是更灵活的替代方案，支持旧版 MongoDB
- BSON 类型（ObjectId、datetime）需自定义 JSON 编码器序列化

## 相关条目

- [[mongodb-query|tools/mongodb-query]]
