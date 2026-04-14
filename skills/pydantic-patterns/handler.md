# Shared Skill: Pydantic Patterns

## Trigger

When defining data models, validating configurations, or serializing/deserializing structured data. Used across Phases 2-7, 9-10. Inspired by agency-agents Backend Architect pattern for type-safe data contracts.

## Required Reading

- `.dev-workflow/shared/skills/project_environment.md` — 命令路径

## Core Patterns

### Pattern 1: Validation Model + Runtime Type Dual Definition

```python
# state.py — 运行时类型（零开销）
class WorkflowState(TypedDict):
    phase: str
    api_changed: bool

# state_schema.py — 校验模型（仅边界处使用）
class WorkflowStateModel(BaseModel):
    phase: Literal["prd", "plan", "dev", "review", "done"]
    api_changed: bool
    model_config = {"extra": "forbid"}
```

**原则**：TypedDict 做日常传递，Pydantic 做边界校验，两者字段保持同步。

### Pattern 2: Constrained Fields

```python
from pydantic import BaseModel, Field

class TaskCard(BaseModel):
    id: str = Field(pattern=r"^T-\d{3}$")          # 正则约束
    complexity: float = Field(ge=0.0, le=1.0)      # 范围约束
    depends_on: list[str] = Field(default_factory=list)  # 可选带默认值
    rejection_count: int = Field(ge=0, default=0)   # 非负整数
```

### Pattern 3: Nested Models

```python
class MemoryConfig(BaseModel):
    local_skills: list[str] = Field(default_factory=list)
    chromadb_access: bool = False

class AgentPlugin(BaseModel):
    name: str
    version: str = Field(pattern=r"^\d+\.\d+\.\d+$")
    memory: MemoryConfig                      # 嵌套模型
    denied_commands: list[str] = Field(default_factory=list)

    model_config = {"extra": "forbid"}
```

### Pattern 4: Enum-Backed Literal Fields

```python
from typing import Literal

# 用 Literal 而非 Enum，保持 JSON 友好
class AgentPluginSchema(BaseModel):
    # 不用: phase: Phase  (Enum 序列化会有问题)
    # 而用: phase: Literal["prd", "plan", "dev", "review", "done"]
    phase: Literal["prd", "plan", "dev", "review", "done"]
```

### Pattern 5: YAML → Pydantic Validation Pipeline

```python
import yaml
from pydantic import ValidationError

def load_and_validate(path: Path, model_class: type[BaseModel]) -> BaseModel:
    """从 YAML 加载并用 Pydantic 校验。"""
    raw = yaml.safe_load(path.read_text())
    try:
        return model_class.model_validate(raw)
    except ValidationError as e:
        # 格式化错误信息便于调试
        for error in e.errors():
            loc = " → ".join(str(l) for l in error["loc"])
            print(f"  {loc}: {error['msg']}")
        raise
```

### Pattern 6: Serialization with Exclusions

```python
class GlobalConfig(BaseModel):
    claude_path: str = "claude"
    chromadb_path: str = ".chroma_db"
    api_key: str = ""  # 敏感字段

    def safe_dump(self) -> dict:
        """序列化时排除敏感字段。"""
        data = self.model_dump()
        if "api_key" in data:
            data["api_key"] = "***"
        return data
```

## Common Validation Recipes

### 校验文件路径存在

```python
from pydantic import field_validator

class ProjectConfig(BaseModel):
    working_dir: str

    @field_validator("working_dir")
    @classmethod
    def validate_path_exists(cls, v: str) -> str:
        if not Path(v).exists():
            raise ValueError(f"Path does not exist: {v}")
        return v
```

### 校验枚举值来自设计文档

```python
class PluginConfig(BaseModel):
    # Literal 约束值域，与设计文档枚举定义保持一致
    platform: Literal["github", "gitlab"]
    mode: Literal["interactive", "auto"]
```

### 默认值从工厂函数

```python
# ❌ 错误：可变默认值
class Config(BaseModel):
    allowed_tools: list[str] = []  # 所有实例共享同一列表！

# ✅ 正确：使用 default_factory
class Config(BaseModel):
    allowed_tools: list[str] = Field(default_factory=list)
```

## Testing Pydantic Models

```python
import pytest
from pydantic import ValidationError

def test_valid_config():
    config = WorkflowStateModel(phase="prd", api_changed=False)
    assert config.phase == "prd"

def test_invalid_enum_value():
    with pytest.raises(ValidationError) as exc_info:
        WorkflowStateModel(phase="invalid", api_changed=False)
    assert "literal" in str(exc_info.value).lower()

def test_extra_field_forbidden():
    with pytest.raises(ValidationError):
        WorkflowStateModel(phase="prd", api_changed=False, extra_field="x")

def test_negative_rejection_count():
    with pytest.raises(ValidationError):
        WorkflowStateModel(phase="prd", api_changed=False, rejection_count=-1)
```

## Rules

- Pydantic Model 仅用于校验边界（磁盘读取、API 输入），运行时用 TypedDict
- 字段约束优先用 `Field()` + `Literal`，不用自定义 validator 除非必要
- 可变默认值必须用 `Field(default_factory=...)`
- `model_config = {"extra": "forbid"}` 防止多余字段
- 测试必须覆盖：合法值、非法值、缺失字段、多余字段
