#!/usr/bin/env python3
"""
AgentFlow Self-Questioning Enforcer — PreToolUse hook
强制在 REFLECT 前（写入 Soul.md 或 Memory.md 时）完成自我质询。

机制：
  self-questioning 完成 → 创建 .self-questioning-done 标记
  Agent 尝试 REFLECT（写入 Soul.md）→ 本 hook 检查标记 → 无标记 = 跳过了自查 = 阻断

铁律 9：VERIFY 后、REFLECT 前必须执行 self-questioning skill。
"""
import json
import os
import sys
import time

# 标记文件
SELF_QUESTIONING_MARKER = ".agent-flow/state/.self-questioning-done"
COMPLEXITY_FILE = ".agent-flow/state/.complexity-level"

# REFLECT 阶段特征：写入这些文件通常意味着正在执行 REFLECT
REFLECT_PATH_KEYWORDS = [
    "memory/main/Soul.md",
    "memory/main/Memory.md",
    "souls/main.md",
]


def is_reflect_operation(file_path: str) -> bool:
    """判断文件写入是否属于 REFLECT 操作"""
    normalized = os.path.normpath(file_path)
    for keyword in REFLECT_PATH_KEYWORDS:
        if keyword in normalized:
            return True
    return False


def has_self_questioning_done() -> bool:
    """检查自我质询是否已完成"""
    if not os.path.isfile(SELF_QUESTIONING_MARKER):
        return False
    try:
        with open(SELF_QUESTIONING_MARKER, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # 标记文件内容格式: timestamp={ISO8601}\ntask={任务描述}
            return bool(content)
    except Exception:
        return False


def get_current_task() -> str:
    """从 current_phase.md 获取当前任务描述"""
    phase_file = ".agent-flow/state/current_phase.md"
    if not os.path.isfile(phase_file):
        return ""
    try:
        with open(phase_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("# 任务:") or line.strip().startswith("# 任务:"):
                    return line.strip().lstrip("# ").strip()
    except Exception:
        pass
    return ""


def main():
    # 只在 agent-flow 项目中生效
    if not os.path.isdir(".agent-flow") and not os.path.isdir(".dev-workflow"):
        sys.exit(0)

    # 只在 pre-flight 完成后执行
    phase_file = ".agent-flow/state/current_phase.md"
    if not os.path.isfile(phase_file) or os.path.getsize(phase_file) <= 10:
        sys.exit(0)

    # 读取 hook 输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只拦截 Write/Edit 到 REFLECT 相关文件
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not is_reflect_operation(file_path):
        sys.exit(0)

    # 检查自我质询是否已完成
    if has_self_questioning_done():
        sys.exit(0)  # 自我质询已完成，放行 REFLECT

    # 未完成自我质询 → 阻断 REFLECT
    task_desc = get_current_task()
    print(
        f"[AgentFlow BLOCKED] 自我质询未完成，禁止执行 REFLECT（写入 Soul.md）！\n"
        f"当前任务: {task_desc or '未知'}\n\n"
        f"铁律 9：VERIFY 后、REFLECT 前必须执行 self-questioning skill。\n\n"
        f"请先执行:\n"
        f"  1. 读取 ~/.agent-flow/skills/workflow/self-questioning/handler.md\n"
        f"  2. 执行 10 项结构化自查（流程合规/知识利用/效率分析/知识缺口）\n"
        f"  3. 将自查报告写入 .agent-flow/state/self-questioning-report.md\n"
        f"  4. 创建标记: 写入 .agent-flow/state/.self-questioning-done\n"
        f"  5. 然后再执行 REFLECT 写入 Soul.md"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
