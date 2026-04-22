# Shared Skill: YAML Configuration

## Trigger

When creating, reading, or validating YAML configuration files. Used in Phases 4 (agent.yaml), 7 (config.yaml, agent-workflow.yaml). Inspired by agency-agents pattern for configuration-driven agent systems.

## Required Reading

- `.dev-workflow/shared/skills/pydantic_patterns.md` — Pydantic 校验模式
- `documents/设计.md` — 配置相关章节

## Configuration Architecture

```
双层配置模型：
  全局配置: ~/.agent-workflow/config.yaml
  项目配置: ./agent-workflow.yaml

合并规则: 项目配置覆盖全局配置
```

## YAML Schema Definitions

### Global Config Schema

```yaml
# ~/.agent-workflow/config.yaml
claude_path: "claude"           # Claude Code CLI 路径
chromadb_path: ".chroma_db"     # ChromaDB 数据目录
log_level: "INFO"               # 日志级别: DEBUG/INFO/WARNING/ERROR
default_mode: "interactive"     # 默认运行模式: interactive/auto
cleanup_retention_days: 7       # 清理保留天数
```

### Project Config Schema

```yaml
# ./agent-workflow.yaml
name: "my-project"
tech_stack:
  frontend: "next.js"
  backend: "python-fastapi"
  database: "postgresql"
package_manager: "pnpm"
git:
  platform: "github"            # github | gitlab
  remote: "origin"
  main_branch: "main"
  develop_branch: "develop"
style:
  framework: "tailwind"
  linting: "eslint"
feishu:
  enabled: true
agents:
  prd:
    enabled: true
  planner:
    enabled: true
  frontend:
    enabled: true
  backend:
    enabled: true
  reviewer:
    enabled: true
```

### Agent Plugin Config Schema

```yaml
# aw/plugins/{agent}/agent.yaml
name: "prd"
version: "1.0.0"
tools:
  - "Read"
  - "Write"
  - "Bash"
  - "Glob"
allowed_paths:
  - "agent-workflow/"
denied_commands:
  - "rm -rf"
  - "DROP TABLE"
on_complete: "commit_and_report"
on_failure: "rollback_and_notify"
memory:
  local_skills: true
  chromadb_access: false
prompt_path: "prompt.md"
soul_path: "soul.md"
skills_dir: "skills/"
```

## YAML Processing Patterns

### Pattern 1: Safe Load + Pydantic Validation

```python
import yaml
from pathlib import Path
from pydantic import BaseModel, ValidationError

def load_config(path: Path, schema: type[BaseModel]) -> BaseModel:
    """安全加载 YAML 并用 Pydantic 校验。"""
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with open(path) as f:
        raw = yaml.safe_load(f)  # safe_load 防止代码注入

    if raw is None:
        raw = {}

    try:
        return schema.model_validate(raw)
    except ValidationError as e:
        errors = []
        for err in e.errors():
            loc = " → ".join(str(l) for l in err["loc"])
            errors.append(f"  {loc}: {err['msg']}")
        raise ValueError(
            f"Config validation failed in {path}:\n" + "\n".join(errors)
        ) from e
```

### Pattern 2: Layered Config Merge

```python
def merge_configs(global_config: dict, project_config: dict) -> dict:
    """项目配置覆盖全局配置（深层合并）。"""
    result = global_config.copy()
    for key, value in project_config.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
    return result
```

### Pattern 3: Default Config Generation

```python
def get_default_global_config() -> dict:
    """返回全局默认配置。"""
    return {
        "claude_path": "claude",
        "chromadb_path": ".chroma_db",
        "log_level": "INFO",
        "default_mode": "interactive",
        "cleanup_retention_days": 7,
    }
```

### Pattern 4: Project Type Detection

```python
def detect_project_type(project_dir: Path) -> dict:
    """扫描项目文件推断技术栈。"""
    indicators = {
        "package.json": {"frontend": "node", "package_manager": "npm"},
        "next.config.*": {"frontend": "next.js"},
        "pyproject.toml": {"backend": "python"},
        "requirements.txt": {"backend": "python"},
        "tailwind.config.*": {"style": {"framework": "tailwind"}},
    }

    result = {}
    for pattern, info in indicators.items():
        if list(project_dir.glob(pattern)):
            result.update(info)
    return result
```

## Testing YAML Config

```python
import pytest
import yaml
from pathlib import Path

def test_load_valid_config(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump({"claude_path": "/usr/bin/claude"}))
    config = load_config(config_file, GlobalConfig)
    assert config.claude_path == "/usr/bin/claude"

def test_load_invalid_yaml(tmp_path):
    config_file = tmp_path / "config.yaml"
    config_file.write_text("invalid: yaml: content:")
    with pytest.raises(yaml.YAMLError):
        yaml.safe_load(config_file.read_text())

def test_missing_config():
    with pytest.raises(FileNotFoundError):
        load_config(Path("/nonexistent"), GlobalConfig)
```

## Rules

- 永远使用 `yaml.safe_load()`，不用 `yaml.load()`（防止代码注入）
- YAML 值必须用 Pydantic 校验，不信任原始输入
- 配置缺失字段应有合理默认值
- 项目配置覆盖全局配置，不反之
- 敏感字段（api_key 等）不写入配置文件，用环境变量
