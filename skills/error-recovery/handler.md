# Skill: Error Recovery & Debugging

## Trigger

When tests fail, commands error, code behaves unexpectedly, or implementation doesn't work as expected. Use also when iterative AI-driven fix loops are needed. Systematic diagnosis over intuition — inspired by DevOps Automator and Incident Response Commander patterns.

## Required Reading

- `.dev-workflow/Agent.md` — 铁律（不确定就停）
- `.dev-workflow/executor/skills/environment_setup.md` — 环境路径问题

## Primary Protocol: OODA Loop

All debugging follows the Observe-Orient-Decide-Act cycle. Each iteration of the loop is one attempt; repeated attempts follow the retry strategy.

### Observe — 收集事实，不做假设

```bash
# 1. 完整阅读错误信息（不跳过 traceback）
# 2. 确认错误类型和位置
$PYTEST agent-workflow/tests/test_{module}.py -v --tb=long

# 3. 复现问题（确认不是偶发）
$PYTEST agent-workflow/tests/test_{module}.py -v -k "test_name"

# 4. 检查相关文件当前状态
# 用 Read 工具查看源码和测试代码
```

Key discipline: read the full error before acting.

```
❌ 错误做法：看到 ImportError 就重新安装包
✅ 正确做法：先读完整错误信息，确认是哪个模块、哪一行、什么原因
```

### Orient — 定位根因

**Error Classification Decision Tree**:

```
错误类型？
├── ImportError / ModuleNotFoundError
│   ├── 模块路径是否正确？ → 检查 __init__.py
│   ├── 包是否安装？ → pip install -e ".[dev]"
│   └── 循环导入？ → 检查交叉引用 → 见"复杂场景: 循环导入"
├── TypeError / AttributeError
│   ├── 对象实际类型？ → print(type(obj))
│   ├── 是否 None？ → 检查初始化
│   └── 方法名拼写？ → 检查 API 文档
├── AssertionError (测试失败)
│   ├── 预期值是什么？ → 读取测试代码
│   ├── 实际值是什么？ → 添加 print 或用 -v 查看
│   └── 是否是测试本身的问题？ → 交叉验证
├── ValidationError (Pydantic)
│   ├── 哪个字段校验失败？ → 读取错误详情
│   ├── 实际传入什么值？ → 打印输入数据
│   └── Schema 是否正确？ → 对比设计文档
├── 路径错误
│   ├── command not found → 检查 environment_setup.md，确认绝对路径
│   └── No such file → 确认文件实际位置
├── Lint 错误 (ruff)
│   └── 读取具体规则名和行号
└── RuntimeError / 自定义异常
    ├── 异常从哪抛出？ → 追踪 traceback
    ├── 触发条件是否合理？ → 检查业务逻辑
    └── 是否需要更明确的错误信息？ → 改进异常消息
```

### Decide — 选择修复方案

| 方案 | 适用场景 | 风险 |
|------|----------|------|
| 修改源码 | 代码逻辑错误 | 可能引入新 bug |
| 修改测试 | 测试预期错误 | 可能掩盖真实问题 |
| 修改配置 | 配置不匹配 | 低 |
| 添加缺失文件 | `__init__.py` 等 | 低 |
| 运行 ruff --fix | 可自动修复的 lint 问题 | 低 |

**原则**：优先修改源码而非测试，除非确认测试预期有误

### Act — 执行并验证

**3-Step Recovery** (within each OODA Act phase):

**Step 1: Read the Error** — already done in Observe.

**Step 2: Classify** — already done in Orient.

**Step 3: Apply Targeted Fix** — minimal change, one point at a time:

**路径问题**（最常见）：

```bash
# 诊断：确认 .venv 位置
ls /Users/sunyi/ai/sunyi-llm/.venv/bin/python

# 修复：使用绝对路径
/Users/sunyi/ai/sunyi-llm/.venv/bin/pytest agent-workflow/tests/ -v
```

**导入问题**：

```bash
# 诊断：确认包已安装
/Users/sunyi/ai/sunyi-llm/.venv/bin/python -c "import aw"

# 修复：重装
cd agent-workflow && /Users/sunyi/ai/sunyi-llm/.venv/bin/pip install -e ".[dev]"
```

**测试失败**：

1. 读取完整 pytest 输出（包括 traceback）
2. 找到第一个失败的测试
3. 对比预期值和实际值
4. 定位到源码具体行
5. 修复后只运行该测试文件验证
6. 全量测试确认无回归

**Lint 失败**：

1. 运行 `ruff check --fix` 自动修复可修复的问题
2. 手动修复剩余问题
3. 不使用 `# noqa` 绕过，除非有充分理由

**Verify Fix — Never Assume**:

```bash
# 修复后必须验证
$PYTEST agent-workflow/tests/ -v
$RUFF check agent-workflow/aw/
```

## Retry Strategy

```
最多重试 3 次（每次都是一轮完整的 OODA 循环）：
  第 1 次：针对性修复（基于错误信息）
  第 2 次：换一种修复思路（如果第1次方向可能不对）
  第 3 次：简化问题（写最小复现案例）
  3 次仍失败 → 暂停，报告 Main Agent 请求帮助
```

## Debugging Anti-Patterns

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| 随机修改试错 | 无方向感，浪费时间 | 先分类错误，再定向修复 |
| 只看最后一个错误 | 可能是连锁反应 | 从第一个错误开始修 |
| 跳过 traceback | 丢失关键线索 | 完整阅读错误堆栈 |
| 修改后不跑全量测试 | 引入回归 | 每次修复后全量验证 |
| 过度修改 | 改了不该改的 | 最小改动原则 |
| 忽略间歇性失败 | 可能是并发/竞态问题 | 多次运行确认 |
| 盲目重试同样操作 | 不会产生不同结果 | 每次重试必须换思路 |

## Complex Debugging Scenarios

### 场景1: 循环导入

```python
# 问题：A 导入 B，B 导入 A
# 诊断：看 ImportError 的具体模块路径
# 修复：使用延迟导入（函数内 import）
def some_function():
    from aw.core.state_schema import WorkflowStateModel  # 延迟导入
```

### 场景2: Async 不一致

```python
# 问题：调用 async 函数没有 await
result = async_function()    # ❌ 返回 coroutine 对象
result = await async_function()  # ✅ 返回实际结果
```

### 场景3: Mock 行为与真实不一致

```python
# 问题：Mock 返回值与真实 API 不匹配
mock.return_value = "string"      # Mock 返回字符串
real_api() → {"key": "value"}    # 真实 API 返回字典
# 修复：Mock 返回值必须与真实行为一致
mock.return_value = {"key": "value"}
```

### 场景4: 测试间状态泄漏

```python
# 问题：测试 A 修改了全局状态，影响测试 B
# 修复：使用 pytest fixture 确保隔离
@pytest.fixture
def fresh_state():
    state = default_workflow_state()
    yield state
    # 清理（如需要）
```

## Iterative Refinement (Complex/Iterative Scenarios)

When a single OODA cycle is insufficient and the task requires repeated AI-driven fix loops, use iterative refinement patterns. This extends the basic 3-retry strategy with structured loop control.

### Choosing a Loop Variant

| 变体 | 完成判定 | 适用场景 | 示例 |
|------|----------|----------|------|
| **信号循环** | AI 输出完成信号（如 `ALL_TASKS_COMPLETE`） | AI 自主迭代，任务间可独立完成 | 逐任务实现直到全部完成 |
| **交互循环** | 用户明确批准 | 需要人工审核确认 | 代码审查后人工确认 |
| **Bash 门控循环** | 外部命令 exit 0 | 有确定性验证标准 | 测试全部通过后停止 |

**选择决策**：
- 有确定性验证标准？→ Bash 门控（最可靠）
- 需要人工把关？→ 交互循环
- 以上都不满足？→ 信号循环（需定义明确的完成信号）

### Context Strategy

**这是迭代循环最关键的架构决策。**

#### Fresh Context（Ralph Pattern）

```
迭代1: 新会话 → 读取 $ARTIFACTS_DIR/plan.md → 执行任务1 → 写入进度文件
迭代2: 新会话 → 读取进度文件 + plan.md → 执行任务2 → 更新进度文件
迭代3: 新会话 → 读取进度文件 + plan.md → ALL_TASKS_COMPLETE
```

- **适用**：每次迭代是独立任务（如逐文件实现不同功能）
- **优点**：避免上下文窗口溢出，每轮聚焦当前任务
- **缺点**：丢失前几轮的推理上下文，需通过文件传递状态

#### Shared Context（Fix-Iterate Pattern）

```
迭代1: 同一会话 → 实现功能 → 运行测试 → 发现失败
迭代2: 同一会话 → 修复问题 → 运行测试 → 仍然失败
迭代3: 同一会话 → 再次修复 → 运行测试 → 通过
```

- **适用**：迭代修复同一问题（如修复审查意见、调试错误）
- **优点**：保留完整推理链，AI 理解修改历史
- **缺点**：长迭代可能上下文溢出

#### Context Decision Tree

```
迭代间任务是否独立？
├── 是 → Fresh Context + 产物文件传递状态
└── 否（修复/改进同一产出）
    ├── 预计迭代次数 ≤ 5 → Shared Context
    └── 预计迭代次数 > 5 → Fresh Context + 错误摘要传递
```

### Iteration Safeguards

每个迭代循环必须有以下防护：

| 防护 | 说明 | 建议值 |
|------|------|--------|
| **硬性上限** | `max_iterations`，超过强制停止 | ≤ 20 |
| **进度指示** | 每轮迭代输出可检查的进度证据 | 完成了什么、还剩什么 |
| **超限升级** | 超过上限时生成摘要报告，升级给人类决策 | 不得静默跳过 |
| **超时保护** | 每轮迭代最大执行时间 | `idle_timeout: 300000`（5 分钟） |

### Bash Gate Control

Bash 门控循环使用确定性脚本判定完成：

```yaml
loop:
  prompt: "Fix the next failing test"
  until: TESTS_PASS
  until_bash: "cd /repo && bun test 2>&1 | tail -1 | grep -q 'all tests passed'"
  max_iterations: 10
```

**判定脚本要求**：
- 必须幂等（多次运行结果一致）
- exit 0 = 完成，非 0 = 未完成
- 不修改任何文件状态

### State Passing for Fresh Context Loops

```
$ARTIFACTS_DIR/
  plan.md         ← 计划文件（迭代前创建）
  progress.json   ← 进度文件（每轮更新）
  changes.md      ← 变更摘要（每轮追加）
```

每轮迭代的提示词模板：

```markdown
读取 $ARTIFACTS_DIR/progress.json 了解当前进度。
读取 $ARTIFACTS_DIR/plan.md 了解完整计划。
执行下一个未完成的任务。
完成后更新 $ARTIFACTS_DIR/progress.json。
如果所有任务完成，输出 ALL_TASKS_COMPLETE。
```

Shared Context 循环无需额外状态传递，但需注意：
- 控制每轮输出的长度，避免上下文膨胀
- 超过 5 轮后评估是否切换为 Fresh Context

## Common Pitfalls Checklist

- [ ] 命令路径是否使用了绝对路径？（最常见问题）
- [ ] 修改文件后是否保存了？
- [ ] 新建包目录是否添加了 `__init__.py`？
- [ ] Pydantic model 和 TypedDict 字段是否同步？
- [ ] 异步函数是否用了 `async def` 和 `await`？
- [ ] Mock 对象是否正确设置了返回值？
- [ ] 测试文件是否 import 了正确的模块？

## Rules

- 诊断先行，修复在后 — 不盲目重试
- 遵循 OODA 循环：Observe → Orient → Decide → Act
- 每次修复只改一个点，改完立即验证
- 修复后必须全量测试，不只是失败的测试
- 3 次重试失败必须上报，不继续死磕
- 迭代循环必须有硬性上限（建议 ≤ 20 次），无上限是设计错误
- 每轮迭代必须产出可检查的进度证据
- Fresh Context 循环必须通过文件（而非会话记忆）传递状态
- 超过迭代上限必须停止并升级，不得静默跳过
- Bash 门控循环的判定脚本必须幂等
- 信号循环的完成信号必须是唯一的、不会在正常输出中意外出现的字符串
- 交互循环的 gate_message 必须明确告知用户需要审核什么
- 记录错误和解决方案到 SOUL.md 动态区
