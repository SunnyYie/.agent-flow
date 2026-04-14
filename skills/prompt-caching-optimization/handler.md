# Skill: 提示词缓存优化策略

> 来源: [claude-cookbooks/misc/prompt_caching.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb)

## Trigger — 何时使用

- 设计或优化 AI Agent 的系统提示词时
- 多步骤 AI 流程中需要减少延迟和成本时
- 多轮对话场景下需要最大化缓存命中时
- 编排者-工作者架构中需要为工作者提供缓存优化上下文时

## Procedure — 执行步骤

### Step 1: 三层缓存架构设计

按稳定性从高到低组织提示词内容，确保缓存命中率最大化：

```
┌──────────────────────────────────────────────┐
│ Layer 1: 系统提示词缓存（跨会话命中）         │
│  - 角色定义、行为准则、全局技能引用           │
│  - rules/*.md 中的铁律和约束                  │
│  - Soul.md 固定区                            │
│  → 标记为 cache_control，每次会话首条即缓存    │
├──────────────────────────────────────────────┤
│ Layer 2: 知识库缓存（任务级命中）             │
│  - Wiki 页面、Skill handler 内容              │
│  - 项目上下文文档（Agent.md）                 │
│  → 按需加载时标记显式断点                      │
├──────────────────────────────────────────────┤
│ Layer 3: 对话上下文缓存（对话内命中）         │
│  - 多轮对话中的历史消息                        │
│  - 当前任务的产物文件                          │
│  → 自动缓存，断点随对话增长前移               │
└──────────────────────────────────────────────┘
```

### Step 2: 系统提示词结构优化

将所有提示词模板重构为"稳定前缀 + 动态后缀"结构：

```markdown
<!-- cache-boundary: 以上为稳定前缀，以下为动态后缀 -->
```

**规则**：
1. 稳定前缀（角色、规则、技能列表）放在 `<!-- cache-boundary -->` 之前
2. 动态后缀（当前任务、上下文数据）放在之后，通过文件引用注入
3. 前缀越长越稳定，缓存命中率越高
4. 绝不在前缀中放置任务相关内容

**示例 — SOUL.md 模板结构**：
```markdown
# Soul: Main Agent

## 固定区（核心性格）          ← 稳定前缀
- 角色: 开发监督与验收者
- 核心原则: 严格验收、不遗漏

## 行为准则                    ← 稳定前缀
1. 启动协议: ...
2. 双验收铁律: ...

<!-- cache-boundary: 以上为稳定前缀，以下为动态后缀 -->

## 当前任务                    ← 动态后缀（运行时填充）
（初始化时为空，任务执行时通过 state 文件注入）

## 动态上下文                  ← 动态后缀
（从 .agent-flow/state/ 读取）
```

### Step 3: 选择缓存策略

根据场景选择自动缓存或显式断点：

| 场景 | 推荐策略 | 理由 |
|------|----------|------|
| 单轮问答 + 大上下文 | 自动缓存（`cache_control` 顶层） | 最简单，一行配置 |
| 多轮对话 | 自动缓存 | 断点自动前移，无需手动管理 |
| 系统提示词独立缓存 | 显式断点（system 块上加 `cache_control`） | 系统提示词独立于消息内容缓存 |
| 多段不同 TTL 内容 | 显式断点（最多 4 个） | 不同段可以有不同缓存策略 |
| 编排者 → 多工作者 | 显式断点 + 投机缓存 | 编排者分析结果可被所有工作者复用 |

**自动缓存用法**（推荐首选）：
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    cache_control={"type": "ephemeral"},  # 一行启用
    system=system_prompt,
    messages=conversation,
)
```

**显式断点用法**（精细控制时）：
```python
response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    system=[
        {
            "type": "text",
            "text": large_system_prompt,
            "cache_control": {"type": "ephemeral"},  # 显式断点
        },
    ],
    messages=messages,
)
```

### Step 4: 投机缓存（Speculative Caching）

当用户开始输入时，立即发送 1-token 请求预热缓存：

```
用户开始输入 → 后台发送 sample_one_token(context + cache_control)
用户继续输入 → 缓存预热完成
用户提交问题 → 使用已预热缓存，TTFT 大幅降低
```

**适用场景**：
- 大上下文文档交互（>1000 tokens）
- 用户需要多次查询同一知识库
- 编排者分解任务后、工作者执行前的间隙

**关键约束**：
- 预热请求和正式请求必须使用完全相同的上下文前缀
- 添加时间戳防止跨会话缓存串扰
- 缓存 TTL 5 分钟，每次命中自动续期

### Step 5: 缓存效果监控

通过 API 响应的 usage 字段监控缓存效果：

```python
def print_cache_stats(response):
    usage = response.usage
    cache_create = getattr(usage, 'cache_creation_input_tokens', 0)
    cache_read = getattr(usage, 'cache_read_input_tokens', 0)

    total_input = usage.input_tokens
    cache_hit_rate = cache_read / total_input if total_input > 0 else 0

    print(f"  输入 tokens:     {total_input}")
    print(f"  缓存写入 tokens: {cache_create}")
    print(f"  缓存读取 tokens: {cache_read}")
    print(f"  缓存命中率:      {cache_hit_rate:.1%}")
```

**目标指标**：
- 首次调用：无缓存命中（预期）
- 第 2 次起：缓存命中率 > 90%
- 成本节省：缓存读取价格仅为标准输入的 0.1x

## Rules — 规则约束

1. **固定前缀优先**：不随任务变化的内容必须放在消息最前面
2. **大文件引用不内联**：超过 1KB 的内容通过文件路径引用，不内联到提示词
3. **不跨会话依赖缓存**：缓存 TTL 5 分钟，不保证跨会话可用
4. **最小可缓存长度**：Sonnet 1024 tokens, Opus/Haiku 4096 tokens
5. **断点上限**：每个请求最多 4 个显式断点（自动缓存占 1 个）
6. **模板变量统一**：所有动态内容使用 `{variable}` 占位符，运行时替换

## 参考来源

- [Prompt Caching 官方文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [claude-cookbooks/prompt_caching.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/misc/prompt_caching.ipynb)
- [claude-cookbooks/speculative_prompt_caching.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/misc/speculative_prompt_caching.ipynb)
