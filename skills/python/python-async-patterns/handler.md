# Shared Skill: Python Async Patterns

## Trigger

When implementing or reviewing async code — subprocess management (Phase 3), LangGraph workflows (Phase 11), concurrent Agent execution (Phase 3/11). Inspired by agency-agents Backend Architect pattern for concurrent system design.

## Required Reading

- `.dev-workflow/shared/skills/project_environment.md` — 命令路径
- `documents/设计.md` — 第6节执行器设计

## Core Patterns

### Pattern 1: Subprocess Management

```python
import asyncio

async def run_command(cmd: list[str], timeout: float = 300) -> str:
    """启动子进程并读取输出，带超时控制。"""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Command failed: {stderr.decode()}")
        return stdout.decode()
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        raise TimeoutError(f"Command timed out after {timeout}s")
```

**使用场景**：ClaudeCodeExecutor（S3.1）、GitHub/GitLab 适配器（S9.x）

### Pattern 2: Semaphore-Concurrent Pool

```python
class ExecutorPool:
    """限制并发数的资源池。"""

    def __init__(self, max_concurrent: int = 3):
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._executors: list[ClaudeCodeExecutor] = []

    async def acquire(self, config: SessionConfig) -> ClaudeCodeExecutor:
        await self._semaphore.acquire()
        executor = ClaudeCodeExecutor(config)
        await executor.start_session()
        self._executors.append(executor)
        return executor

    async def release(self, executor: ClaudeCodeExecutor) -> None:
        await executor.close_session()
        self._executors.remove(executor)
        self._semaphore.release()

    async def close_all(self) -> None:
        for executor in list(self._executors):
            await executor.close_session()
        self._executors.clear()
```

**使用场景**：ExecutorPool（S3.3）、并行开发 Agent（S10.5/S10.6）

### Pattern 3: Retry with Exponential Backoff

```python
async def retry_with_backoff(
    func,
    max_retries: int = 2,
    base_delay: float = 1.0,
):
    """带指数退避的重试。"""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                await asyncio.sleep(delay)
    raise last_error
```

**使用场景**：Executor 会话重试（S3.2）、网络请求

### Pattern 4: Line-Protocol Stream Reader

```python
async def read_lines(stream: asyncio.StreamReader) -> AsyncIterator[str]:
    """逐行读取子进程输出（newline-delimited JSON）。"""
    while True:
        line = await stream.readline()
        if not line:
            break
        yield line.decode().strip()
```

**使用场景**：ClaudeCodeExecutor 读取 CLI 输出（S3.1）

### Pattern 5: Graceful Shutdown

```python
async def graceful_shutdown(pool: ExecutorPool, timeout: float = 10.0):
    """优雅关闭所有资源，带超时。"""
    try:
        await asyncio.wait_for(pool.close_all(), timeout=timeout)
    except asyncio.TimeoutError:
        # 超时后强制终止
        for executor in pool._executors:
            executor._process.kill()
```

## Testing Async Code

### Mock Async Functions

```python
from unittest.mock import AsyncMock

# 创建异步 Mock
mock_executor = AsyncMock()
mock_executor.start_session.return_value = "session-123"
mock_executor.send_message.return_value = "response"

# 在测试中使用
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function(mock_executor)
    assert result is not None
```

### Test Concurrent Execution

```python
@pytest.mark.asyncio
async def test_concurrent_limit():
    pool = ExecutorPool(max_concurrent=2)

    async def slow_task():
        executor = await pool.acquire(config)
        await asyncio.sleep(0.1)
        await pool.release(executor)

    # 第三个任务应等待
    tasks = [slow_task() for _ in range(3)]
    await asyncio.gather(*tasks)
```

## Async Anti-Patterns

| 反模式 | 问题 | 正确做法 |
|--------|------|----------|
| `asyncio.run()` 在已有事件循环中 | 嵌套事件循环崩溃 | 使用 `await` 或 pytest-asyncio |
| 忘记 `await` | 返回 coroutine 对象而非结果 | 所有 async 调用必须 await |
| 阻塞操作在 async 中 | 阻塞事件循环 | 用 `asyncio.to_thread()` 包装 |
| 共享状态无锁 | 并发竞态条件 | 使用 `asyncio.Lock` |
| 不处理 `CancelledError` | 任务取消时资源泄漏 | 用 try/finally 清理 |

## Rules

- 所有 I/O 操作必须用 async/await
- 共享资源必须加锁（asyncio.Lock/Semaphore）
- 子进程必须设置超时，防止无限挂起
- 测试 async 代码用 `@pytest.mark.asyncio`（已配置 asyncio_mode="auto"）
- Mock async 函数用 `AsyncMock`，不用普通 `Mock`
