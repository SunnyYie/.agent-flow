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

使用 pymongo 查询 MongoDB（mongosh 不兼容旧版 MongoDB 3.4，详见 [[mongosh-wire-version|pitfalls/tools/mongosh-wire-version]]）。

## 快速上手

```python
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime, date

# 自定义 JSON 编码器，处理 BSON 特有类型（ObjectId, datetime）
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

**注意**：pymongo 返回的文档包含 BSON 特有类型，必须用自定义 JSON 编码器处理 ObjectId 和 datetime，否则 `json.dumps` 会报 TypeError。

## 完整查询 SOP

详见 [[mongodb-query-skill|skills/research/mongodb-query/handler]] — 包含分步过程、规则、故障排除和更多查询模式。

## 相关条目

- [[mongodb-query-skill|skills/research/mongodb-query/handler]] — MongoDB 查询 Skill（权威操作参考）
- [[mongosh-wire-version|pitfalls/tools/mongosh-wire-version]] — mongosh 兼容性踩坑
