# Shared Skill: Testing Strategies

## Trigger

When writing tests beyond basic unit tests — integration, e2e, mocking, and async testing. Used across all phases, critical for Phase 14 (e2e testing). Inspired by agency-agents Test Results Analyzer and Reality Checker patterns.

## Required Reading

- `.dev-workflow/shared/skills/project_environment.md` — 命令路径
- `.dev-workflow/shared/skills/python_async_patterns.md` — 异步测试

## Testing Pyramid for This Project

```
        ╱  E2E  ╲           Phase 14 — 端到端工作流测试
       ╱─────────╲          少量，慢，高价值
      ╱ Integration ╲       Phase 11-13 — 子图集成、CLI 集成
     ╱───────────────╲      适量，中等速度
    ╱   Unit Tests    ╲     Phase 2-10 — 每个模块的单元测试
   ╱───────────────────╲    大量，快，基础保障
```

## Test Categories

### 1. Unit Tests (Phases 2-10)

**每个模块的单元测试**：

```python
# tests/test_{module}.py

class Test{ModuleName}:
    """测试 {module} 的核心功能。"""

    def test_happy_path(self):
        """正常输入返回预期结果。"""

    def test_empty_input(self):
        """空输入的处理。"""

    def test_invalid_input(self):
        """非法输入抛出正确异常。"""

    def test_boundary_value(self):
        """边界值（0、最大值、空列表等）。"""

    def test_default_values(self):
        """默认值正确。"""
```

### 2. Integration Tests (Phases 11-13)

**子图/组件间交互测试**：

```python
# tests/integration/test_{feature}.py
import pytest

class Test{Feature}Integration:
    """测试 {feature} 的组件间交互。"""

    @pytest.fixture
    def mock_executor(self):
        """提供 Mock 的执行器。"""
        return AsyncMock(spec=ClaudeCodeExecutor)

    @pytest.mark.asyncio
    async def test_subgraph_end_to_end(self, mock_executor):
        """子图从 START 到 END 的完整流程。"""
        # 设置 Mock 行为
        mock_executor.send_message.return_value = "mock response"

        # 执行子图
        result = await run_subgraph(initial_state, mock_executor)

        # 验证输出状态
        assert result["phase"] == "plan"
        assert result["prd_path"] != ""
```

### 3. E2E Tests (Phase 14)

**完整工作流端到端测试**：

```python
# tests/e2e/test_full_workflow.py
import pytest

class TestFullWorkflow:
    """端到端工作流测试。"""

    @pytest.fixture
    def sample_input(self, tmp_path):
        """准备测试输入文件。"""
        input_file = tmp_path / "sample_prd.md"
        input_file.write_text("# 首页添加计数器按钮\n...")
        return str(input_file)

    @pytest.mark.asyncio
    @pytest.mark.timeout(600)
    async def test_local_file_workflow(self, sample_input):
        """本地文件输入的完整工作流。"""
        result = await run_workflow(
            source="local",
            doc_url=sample_input,
            auto=True,
        )
        assert result["phase"] == "done"
```

## Mocking Strategies

### Strategy 1: Subprocess Mock (for CLI adapters)

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_github_create_mr():
    with patch("asyncio.create_subprocess_exec") as mock_proc:
        mock_proc.return_value.communicate = AsyncMock(
            return_value=(b"https://github.com/owner/repo/pull/1", b"")
        )
        mock_proc.return_value.returncode = 0

        adapter = GitHubAdapter("owner/repo")
        url = await adapter.create_mr("feature", "develop", "Title", "Desc")
        assert "pull" in url
```

### Strategy 2: File System Mock (for memory/config)

```python
def test_memory_manager(tmp_path):
    """使用 tmp_path 隔离文件系统。"""
    manager = MemoryManager(tmp_path, "prd")
    manager.write_memory("test content")
    assert manager.read_memory() == "test content"
```

### Strategy 3: Pydantic Model as Test Data Factory

```python
def make_workflow_state(**overrides) -> dict:
    """创建测试用 WorkflowState，可覆盖任意字段。"""
    defaults = default_workflow_state()
    defaults.update(overrides)
    return defaults

# 使用
state = make_workflow_state(phase="dev", api_changed=True)
```

### Strategy 4: Claude Code Executor Mock

```python
@pytest.fixture
def mock_executor():
    """Mock ClaudeCodeExecutor 的标准 fixture。"""
    executor = AsyncMock(spec=ClaudeCodeExecutor)
    executor.start_session.return_value = "session-123"
    executor.is_alive.return_value = True
    executor.send_message.return_value = "mock response"
    return executor
```

## Test Organization

```
agent-workflow/tests/
├── conftest.py              # 全局 fixtures
├── test_scaffold.py         # 冒烟测试
├── test_state.py            # 单元测试
├── test_executor.py         # 单元测试（含 Mock）
├── integration/             # 集成测试
│   ├── test_prd_subgraph.py
│   └── test_dev_subgraph.py
├── e2e/                     # 端到端测试
│   ├── test_full_workflow.py
│   ├── test_rejection_loop.py
│   └── test_cancel_resume.py
└── security/                # 安全测试
    └── test_security_layers.py
```

## Coverage Targets

| 阶段 | 目标覆盖率 | 重点 |
|------|-----------|------|
| Phase 2-5 | 80%+ | 核心模块全面覆盖 |
| Phase 6-7 | 90%+ | 安全层和配置必须有高覆盖 |
| Phase 8-9 | 80%+ | CLI 和 Git 适配器 Mock 测试 |
| Phase 10 | 70%+ | Agent 插件逻辑测试 |
| Phase 11 | 60%+ | LangGraph 集成测试 |
| Phase 14 | 关键路径 100% | E2E 端到端覆盖 |

## Rules

- 外部依赖必须 Mock（LLM 调用、子进程、网络请求、文件系统用 tmp_path）
- 每个测试只验证一个行为
- 测试命名：`test_{what}_{condition}_{expected}`
- 异步测试用 `@pytest.mark.asyncio`（已配置 auto mode）
- 集成/E2E 测试放在对应子目录，标记 `@pytest.mark.integration`
- 不为测试而测试——每个测试必须验证有意义的行为

## Quality Gate — 测试矩阵5维检查

> 建立测试验收矩阵时必须执行5维检查，详见 `wiki/patterns/workflow/test-matrix-5-dimension-check.md`

| 维度 | 核心要求 |
| ---- | -------- |
| 覆盖度 | 每个原始问题必须有直接验收项+量化通过标准 |
| 可追溯 | 验收项→原问题→冻结约束可双向反查 |
| 自动化映射 | automated_test验收项映射到 `文件名::用例名` |
| 边界场景 | 每模块至少3个边界用例（冲突/过期/重复） |
| 双验收 | 复杂度≥Medium需双Agent独立审查 |

联调脚本结构规范见 `wiki/patterns/workflow/e2e-script-three-part-structure.md`
