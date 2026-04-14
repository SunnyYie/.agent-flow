---
name: speculative-caching
category: patterns
confidence: 0.85
sources:
  - claude-cookbooks/misc/speculative_prompt_caching.ipynb
tags: [caching, performance, latency, speculative]
---

# Pattern: 投机提示词缓存

## 问题

用户在大型上下文（如知识库、代码库）中交互时，首次查询需要等待缓存创建 + 响应生成，导致高 TTFT（Time To First Token）。

## 解决方案

在用户输入期间，后台发送 1-token 请求预热缓存。用户提交时缓存已就绪，直接命中。

### 工作流程

```
无投机缓存:
  用户输入(3s) → 提交 → 缓存创建 + 响应生成（高 TTFT）

有投机缓存:
  用户开始输入 → 后台 1-token 预热请求
  用户继续输入 → 缓存预热完成
  用户提交 → 缓存命中 + 响应生成（低 TTFT）
```

### 实现模式

```python
async def speculative_cache_warmup(client, context_message):
    """在用户输入期间后台预热缓存。"""
    await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1,  # 仅采样 1 token
        cache_control={"type": "ephemeral"},
        messages=[context_message],
    )

# 用户开始输入时启动预热
cache_task = asyncio.create_task(speculative_cache_warmup(client, ctx))
# ... 用户输入 ...
await cache_task  # 确保预热完成
# 正式请求，缓存已就绪
```

### 适用场景

- Agent 编排者分解任务后、工作者执行前的等待间隙
- 大型文档/代码库的交互式查询
- 用户在输入框聚焦时即可开始预热

### 关键约束

1. 预热和正式请求必须使用**完全相同**的上下文前缀
2. 添加时间戳防止跨会话缓存串扰
3. 缓存 TTL 5 分钟，超时后预热无效
4. 仅对 >1024 tokens 的上下文有意义（Sonnet 最小可缓存长度）

### 效果

- TTFT 降低 30-60%（取决于上下文大小）
- 总响应时间降低 20-40%
- 额外成本：1-token 预热请求（可忽略）

## 相关

- [提示词缓存](prompt-caching.md)
- [AI 上下文管理](~/.agent-flow/skills/ai-context-management/handler.md)
