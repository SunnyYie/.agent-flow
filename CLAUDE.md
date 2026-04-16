

## Wiki 知识库查询手册

> Agent 查找知识时必须遵循三级查找流程，从 O(1) 到 O(N)：

### 查找流程（必须按顺序执行）

1. **主题枢纽**（O(1)，首选）：`Read ~/.agent-flow/wiki/topics/{keyword}.md`
   → 一次读取获取该主题的全部 patterns + pitfalls + concepts + tools 链接
   → 如主题枢纽存在，直接按链接读取相关文档，**跳过后续步骤**

2. **标签索引**（O(1)，次选）：`Grep "{keyword}" ~/.agent-flow/wiki/TAG-INDEX.md`
   → 在标签索引表中精确匹配 tag，获取所有相关文档路径
   → 适合无主题枢纽的关键词查找

3. **全量搜索**（兜底）：`Grep "{keyword}" ~/.agent-flow/wiki/`
   → 仅在主题枢纽和标签索引均无匹配时使用
   → 扫描全部 wiki 文件，效率最低

### 可用主题枢纽

| 主题 | 路径 | 覆盖范围 |
|------|------|---------|
| workflow | `wiki/topics/workflow.md` | 工作流执行、质量门控（20篇） |
| llm-coding | `wiki/topics/llm-coding.md` | LLM编程原则、踩坑（10篇） |
| feishu | `wiki/topics/feishu.md` | 飞书模式、踩坑、工具（3篇） |
| multi-agent | `wiki/topics/multi-agent.md` | 多Agent协作模式（8篇） |
| agent-flow-cli | `wiki/topics/agent-flow-cli.md` | AgentFlow CLI踩坑（6篇） |
| architecture | `wiki/topics/architecture.md` | 架构模式、决策（7篇） |
| security | `wiki/topics/security.md` | 安全踩坑、权限（2篇） |
| react-native | `wiki/topics/react-native.md` | RN踩坑（2篇） |

### 示例

```
# 查找飞书知识 → 直接读主题枢纽
Read ~/.agent-flow/wiki/topics/feishu.md

# 查找缓存策略 → 先查标签索引
Grep "caching" ~/.agent-flow/wiki/TAG-INDEX.md

# 查找未知主题 → 全量搜索兜底
Grep "关键词" ~/.agent-flow/wiki/
```

### 项目级 Wiki

项目 Wiki 路径：`.agent-flow/wiki/` 或 `.dev-workflow/wiki/`
查找顺序：先项目 Wiki → 再全局 Wiki（`~/.agent-flow/wiki/`）

## Skills 技能查询手册

> Agent 查找技能时必须遵循三级查找流程，与 Wiki 查找一致：

### 查找流程（必须按顺序执行）

1. **主题枢纽**（O(1)，首选）：`Read ~/.agent-flow/skills/topics/{keyword}.md`
   → 一次读取获取该主题的全部技能链接和说明
   → 如主题枢纽存在，直接按链接读取相关技能，**跳过后续步骤**

2. **标签索引**（O(1)，次选）：`Grep "{keyword}" ~/.agent-flow/skills/TAG-INDEX.md`
   → 在标签索引表中精确匹配 tag，获取所有相关技能路径
   → 适合无主题枢纽的关键词查找

3. **全量搜索**（兜底）：`Grep "{keyword}" ~/.agent-flow/skills/`
   → 仅在主题枢纽和标签索引均无匹配时使用

### 可用主题枢纽

| 主题 | 路径 | 技能数 |
|------|------|--------|
| workflow | `skills/topics/workflow.md` | 8个（任务流程控制） |
| agent-orchestration | `skills/topics/agent-orchestration.md` | 5个（多Agent编排） |
| knowledge | `skills/topics/knowledge.md` | 5个（知识管理） |
| development | `skills/topics/development.md` | 7个（代码开发） |
| git | `skills/topics/git.md` | 2个（Git操作） |
| integration | `skills/topics/integration.md` | 4个（外部集成） |
| ai-optimization | `skills/topics/ai-optimization.md` | 5个（AI优化） |
| documentation | `skills/topics/documentation.md` | 4个（文档处理） |
| python | `skills/topics/python.md` | 3个（Python模式） |
| research | `skills/topics/research.md` | 4个（研究搜索） |

### 示例

```
# 查找工作流技能 → 直接读主题枢纽
Read ~/.agent-flow/skills/topics/workflow.md

# 查找Jira操作技能 → 先查标签索引
Grep "jira" ~/.agent-flow/skills/TAG-INDEX.md

# 查找未知技能 → 全量搜索兜底
Grep "关键词" ~/.agent-flow/skills/
```
