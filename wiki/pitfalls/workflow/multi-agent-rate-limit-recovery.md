# Pitfall: 多Agent并行时速率限制导致产出缺失

> 多Agent并行执行时，子Agent因API速率限制(429)失败后，主Agent必须检查产出文件是否存在并自行兜底。
> 来源：Maiya V1.5 步骤18执行实践，4个并行Agent中2个因429失败。

## 踩坑场景

```
主Agent派发4个并行子Agent：
├── Agent 1（文档）→ 成功 ✅
├── Agent 2（服务端测试）→ 成功 ✅（延迟较长）
├── Agent 3（前端测试）→ 429 Rate Limit ❌（0个工具调用成功）
└── Agent 4（联调脚本）→ 429 Rate Limit ❌（0个工具调用成功）

结果：3个期望产出文件中2个不存在
```

## 根因

1. **429错误是瞬时性的**：子Agent收到429后直接退出，不重试
2. **主Agent假设子Agent成功**：只检查Agent返回状态，不检查产出文件是否存在
3. **并行Agent越多，429概率越高**：4个Agent同时请求API，容易触发速率限制

## 正确做法

### 1. 主Agent必须用Glob检查产出文件

```typescript
// 子Agent完成后，立即检查产出文件
const files = Glob('packages/my-server/src/service/agent/__tests__/step18-*.ts');
if (files.length === 0) {
  // 产出文件不存在，主Agent必须自行创建
  console.error('子Agent失败，主Agent兜底创建文件');
  // ... 自行创建文件
}
```

### 2. 不要等待重试

```
❌ 错误：等待几秒后重新派发子Agent
✅ 正确：主Agent直接自行完成，效率更高
```

原因：
- 429冷却时间不确定（可能30秒到5分钟）
- 重试仍然可能429
- 主Agent自行完成更快（避免上下文切换开销）

### 3. 减少并行Agent数量

```
❌ 4个并行Agent → 429概率高
✅ 2-3个并行Agent → 429概率低

策略：
├── 优先合并相似任务（文档+脚本可合并为一个Agent）
├── 高价值任务先行（测试代码优先于文档）
└── 非关键任务放后台（run_in_background: true）
```

### 4. 子Agent提示词精简

```
❌ 子Agent提示词过长（>2000 tokens）→ 多轮API调用 → 429
✅ 子Agent提示词精简（<1000 tokens）→ 少轮API调用 → 降低429风险
```

## 检查清单

- [ ] 子Agent完成后，用Glob检查期望产出文件是否存在
- [ ] 不存在的文件，主Agent自行创建（不要重新派发子Agent）
- [ ] 并行Agent数量≤3（经验值）
- [ ] 子Agent提示词尽量精简，减少API调用轮次
- [ ] 关键产出物优先在前台Agent中完成，非关键的可放后台

## 与orchestrator-worker模式的关系

本踩坑是 `orchestrator-worker` 模式的运维级补充：
- `orchestrator-worker` 定义了"编排者→工作者"的分工模式
- 本踩坑补充了"工作者失败时编排者的兜底策略"
- 核心原则：**不假设工作者一定成功，编排者必须有兜底能力**
