#!/usr/bin/env python3
"""
AgentFlow Subtask Guard Enforcer — PreToolUse hook
强制执行 subtask-guard：每次代码修改前检查是否执行了子任务搜索守卫。

核心机制：
  Agent 执行 subtask-guard → search-tracker.py 创建 .subtask-guard-done 标记
  Agent 执行代码修改 → 本 hook 检查标记 → 无标记 = 没搜索 = 阻断

标记有效期：
  Simple:  30 分钟
  Medium:  15 分钟
  Complex: 10 分钟

仅对代码文件修改生效，不影响 agent-flow 文档、README 等。
"""
import json
import os
import sys
import time

MARKER_FILE = ".agent-flow/state/.subtask-guard-done"
COMPLEXITY_FILE = ".agent-flow/state/.complexity-level"

# 各复杂度的标记有效期（秒）
MAX_AGE_MAP = {
    "simple": 1800,   # 30 分钟
    "medium": 900,    # 15 分钟
    "complex": 600,   # 10 分钟
}
DEFAULT_MAX_AGE = 900

# 代码文件扩展名
CODE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".py", ".rs", ".go", ".java", ".kt",
    ".swift", ".m", ".h", ".c", ".cpp", ".rb", ".php", ".vue", ".svelte",
    ".css", ".scss", ".less", ".html", ".sql", ".graphql",
    ".sh", ".bash", ".zsh",
}

CODE_FILENAMES = {
    "package.json", "tsconfig.json", "Makefile", "Dockerfile",
    "Podfile", "Gemfile", "build.gradle", "settings.gradle",
    "app.json", "babel.config.js", "metro.config.js",
}

# 允许的路径前缀（不受 subtask-guard 检查限制）
ALLOWED_PATH_PREFIXES = (".agent-flow", ".dev-workflow", ".claude")

GUARD_PROMPT = """[AgentFlow BLOCKED] Subtask-guard 未执行 — 你没有在修改代码前搜索知识库！

按 subtask-guard 技能执行（硬性要求，不可跳过）:
  ┌───────────────────────────────────────────────────┐
  │ Step 1: 从 current_phase.md 提取子任务关键词      │
  │ Step 2: 快速搜索（4步，全部必执行）                │
  │   1. Grep "{关键词}" .agent-flow/skills/          │
  │   2. Grep "{关键词}" ~/.agent-flow/skills/        │
  │   3. Grep "{关键词}" .agent-flow/memory/main/Soul.md │
  │   4. Grep "{关键词}" .agent-flow/wiki/ + 全局wiki │
  │ Step 3: 代码定位（涉及代码修改的必须执行）         │
  │ Step 4: 选择执行方式（Skill > Agent > Command）   │
  │ Step 5: 按搜索结果+执行方式执行                   │
  │ Step 6: 记录到 Memory.md                          │
  └───────────────────────────────────────────────────┘

执行搜索后，.subtask-guard-done 标记会自动创建。"""


def get_complexity_level() -> str:
    if not os.path.isfile(COMPLEXITY_FILE):
        return "medium"
    try:
        with open(COMPLEXITY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("level="):
                    level = line.split("=", 1)[1].strip().lower()
                    if level in ("simple", "medium", "complex"):
                        return level
    except Exception:
        pass
    return "medium"


def get_max_age() -> int:
    level = get_complexity_level()
    return MAX_AGE_MAP.get(level, DEFAULT_MAX_AGE)


def is_code_file(file_path: str) -> bool:
    for prefix in ALLOWED_PATH_PREFIXES:
        if prefix in file_path:
            return False
    _, ext = os.path.splitext(file_path)
    if ext.lower() in (".md", ".txt", ".rst", ".adoc"):
        return False
    if ext.lower() in CODE_EXTENSIONS:
        return True
    if os.path.basename(file_path) in CODE_FILENAMES:
        return True
    return False


def has_valid_guard() -> bool:
    if not os.path.isfile(MARKER_FILE):
        return False
    try:
        mtime = os.path.getmtime(MARKER_FILE)
        age = time.time() - mtime
        return age < get_max_age()
    except Exception:
        return False


def main():
    # 只在 agent-flow 项目中生效
    if not os.path.isdir(".agent-flow") and not os.path.isdir(".dev-workflow"):
        sys.exit(0)

    # 只在 pre-flight 完成后执行
    # 同时检查两个路径
    phase_files = [
        ".agent-flow/state/current_phase.md",
        ".dev-workflow/state/current_phase.md",
    ]
    phase_found = any(
        os.path.isfile(pf) and os.path.getsize(pf) > 10
        for pf in phase_files
    )
    if not phase_found:
        sys.exit(0)

    # 读取 hook 输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只拦截 Write 和 Edit
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # 只拦截代码文件
    if not is_code_file(file_path):
        sys.exit(0)

    # 检查 subtask-guard 标记
    if has_valid_guard():
        sys.exit(0)  # 已执行，放行

    # 无标记 → 阻断
    print(f"{GUARD_PROMPT}\n目标文件: {file_path}")
    sys.exit(2)


if __name__ == "__main__":
    main()
