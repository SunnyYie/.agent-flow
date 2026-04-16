#!/usr/bin/env python3
"""Ensure project bootstrap files exist before deeper workflow checks run.

Also injects Wiki Usage Manual into project CLAUDE.md so every Agent
knows how to efficiently query the knowledge base.
"""

import os
from pathlib import Path


# --- Wiki 使用手册模板 ---
WIKI_USAGE_SECTION = """
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
"""


def find_project_root() -> Path | None:
    """Find project root by looking for .agent-flow/ or .dev-workflow/ markers."""
    cwd = Path.cwd()
    # Walk up from cwd to find project root
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".agent-flow").exists() or (parent / ".dev-workflow").exists():
            return parent
        # Don't go beyond home directory
        if parent == Path.home():
            break
    return None


def ensure_wiki_usage_in_claude_md(project_root: Path) -> None:
    """Ensure Wiki Usage Manual section exists in project CLAUDE.md.

    If the section already exists, skip. Otherwise, append it.
    """
    claude_md_path = project_root / "CLAUDE.md"

    # Read existing content
    if claude_md_path.exists():
        try:
            existing = claude_md_path.read_text(encoding="utf-8")
        except Exception:
            return
    else:
        existing = ""

    # Check if wiki usage section already exists
    if "## Wiki 知识库查询手册" in existing:
        return

    # Append wiki usage section
    try:
        new_content = existing.rstrip() + "\n" + WIKI_USAGE_SECTION
        claude_md_path.write_text(new_content, encoding="utf-8")
    except Exception:
        pass


def main() -> None:
    # Try to use agent_flow package if available
    try:
        from agent_flow.core.config import ensure_project_claude_md, ensure_project_mcp_config
        from agent_flow.core.state_contract import find_project_root as af_find_root

        project_root = af_find_root(Path.cwd()) or Path.cwd()
        has_workflow = (project_root / ".agent-flow").exists() or (project_root / ".dev-workflow").exists()
        if has_workflow:
            ensure_project_claude_md(project_root)
            ensure_project_mcp_config(project_root)
    except Exception:
        pass

    # Always ensure wiki usage manual is in CLAUDE.md
    project_root = find_project_root()
    if project_root:
        ensure_wiki_usage_in_claude_md(project_root)


if __name__ == "__main__":
    main()
