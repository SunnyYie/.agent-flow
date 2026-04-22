---
name: mongodb-query
version: 1.0.0
trigger: mongodb, mongo, pymongo, 数据库查询, 留资
applicable_agents: [main, researcher, coder]
confidence: 0.8
abstraction: universal
created: 2026-04-16
---

# Skill: MongoDB 数据查询

## Trigger
当需要查询 MongoDB 数据时触发，尤其是：
- 需要查询留资数据（maiya_lead_forms）
- mongosh 因版本不兼容无法连接时
- 需要用 Python 脚本查询 MongoDB

## Required Reading
- `~/.agent-flow/wiki/pitfalls/tools/mongosh-wire-version.md` — mongosh 版本兼容性问题

## Procedure
1. 检查 mongosh 可用性：`which mongosh`
2. **如果 mongosh 连接失败（wire version 报错）**，改用 pymongo：
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

   client = MongoClient(URI, serverSelectionTimeoutMS=5000)
   db = client['dbname']
   # 执行查询...
   for doc in results:
       print(json.dumps(doc, cls=DateEncoder, indent=2, ensure_ascii=False))
   ```
3. page_id 查询时注意：可能是字符串或 ObjectId，两种都尝试
4. 输出使用 DateEncoder 处理 BSON 类型序列化

## Rules
- 连接旧版 MongoDB（<4.2）时必须用 pymongo，不要尝试 mongosh
- 查询结果中的 ObjectId 和 datetime 必须用自定义编码器序列化
- 不要在命令行参数中暴露完整连接字符串，使用环境变量或代码内传入
