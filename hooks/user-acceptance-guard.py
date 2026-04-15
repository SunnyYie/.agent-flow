#!/usr/bin/env python3
"""
AgentFlow User Acceptance Guard — PreToolUse hook
强制在 git push / MR 创建 / PR 创建 前完成用户验收。

机制：
  每个开发阶段（Research/Plan/Implement）完成后 → Agent 请求用户验收
  → 用户确认"验收通过" → Agent 创建 .user-acceptance-done 标记
  → 本 hook 检查标记 → 无标记 = 未验收 = 阻断 push/MR

按复杂度分级：
  Simple:  提醒但不阻断（用户已确认过实施计划即可）
  Medium:  硬阻断，必须有验收标记
  Complex: 硬阻断，且验收标记必须包含全部3个阶段的确认
"""
import json
import os
import sys

from contract_utils import (
    find_project_root,
    get_complexity_level,
    load_marker_entries,
    read_state_path,
)

# 需要拦截的命令前缀
BLOCKED_COMMANDS = [
    "git push",
    "glab mr create",
    "glab api --method POST",
    "gh pr create",
]

def check_phase_acceptance(marker_path, phase: str) -> bool:
    for entry in load_marker_entries(marker_path):
        if (
            entry.get("phase") == phase
            and entry.get("status") == "accepted"
            and all(entry.get(key, "").strip() for key in ("timestamp", "task", "confirmed_by", "summary"))
        ):
            return True
    return False


def is_blocked_command(command: str) -> bool:
    """判断命令是否为需要拦截的 push/MR 命令"""
    cmd = command.strip()
    for blocked in BLOCKED_COMMANDS:
        if cmd.startswith(blocked):
            return True
    return False


def main():
    project_root = find_project_root()
    if project_root is None:
        sys.exit(0)

    phase_file = read_state_path(project_root, "current_phase.md")
    if not os.path.isfile(phase_file) or os.path.getsize(phase_file) <= 10:
        sys.exit(0)

    # 读取 hook 输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    needs_check = False

    # Bash: 拦截 git push 和 MR 创建命令
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if is_blocked_command(command):
            needs_check = True

    if not needs_check:
        sys.exit(0)

    # 检查用户验收标记
    acceptance_marker = read_state_path(project_root, ".user-acceptance-done")
    has_any_acceptance = any(
        entry.get("status") == "accepted"
        and all(entry.get(key, "").strip() for key in ("phase", "timestamp", "task", "confirmed_by", "summary"))
        for entry in load_marker_entries(acceptance_marker)
    )

    if has_any_acceptance:
        complexity = get_complexity_level(project_root)
        # Complex 任务需要检查每个阶段
        if complexity == "complex":
            missing = []
            if not check_phase_acceptance(acceptance_marker, "research"):
                missing.append("Research")
            if not check_phase_acceptance(acceptance_marker, "plan"):
                missing.append("Plan")
            if not check_phase_acceptance(acceptance_marker, "implement"):
                missing.append("Implement")

            if not missing:
                sys.exit(0)  # 全部阶段验收通过

            # 部分阶段未验收
            missing_str = "\n".join(f"  - {p} 阶段未验收" for p in missing)
            print(
                f"[AgentFlow BLOCKED] Complex 任务需要所有阶段(Research/Plan/Implement)"
                f"的用户验收才能推送代码！\n"
                f"缺少验收的阶段：\n{missing_str}\n\n"
                f"请先执行用户验收：\n"
                f"  1. 向用户展示当前阶段产出\n"
                f"  2. 获得用户明确确认\n"
                f"  3. 写入标记: .agent-flow/state/.user-acceptance-done\n"
                f"     格式: research=accepted\\nplan=accepted\\nimplement=accepted\\n"
                f"  4. 再次尝试推送"
            )
            sys.exit(2)
        else:
            sys.exit(0)  # Simple/Medium 有验收标记即可

    # 无验收标记
    complexity = get_complexity_level(project_root)

    if complexity == "simple":
        # Simple 任务：软提醒
        print(
            "[AgentFlow REMINDER] 即将推送代码，但用户验收未完成！\n"
            "Simple 任务建议：确认用户已看过变更内容并同意推送。\n"
            "创建验收标记: 写入结构化的 .agent-flow/state/.user-acceptance-done"
        )
        sys.exit(0)
    else:
        # Medium/Complex 任务：硬阻断
        print(
            "[AgentFlow BLOCKED] 用户验收未完成，禁止推送代码或创建 MR！\n\n"
            "必须先完成用户验收：\n"
            "  1. 向用户展示变更摘要和测试结果\n"
            "  2. 明确告知影响范围和回滚方案\n"
            "  3. 获得用户明确确认（如'可以推送'、'验收通过'）\n"
            "  4. 写入标记: .agent-flow/state/.user-acceptance-done\n"
            "     每条记录至少包含:\n"
            "     phase=implement|plan|research\n"
            "     status=accepted\n"
            "     timestamp=ISO8601\n"
            "     task=当前任务\n"
            "     confirmed_by=user\n"
            "     summary=用户确认摘要\n\n"
            "  5. 再次尝试推送\n\n"
            "⚠️ 禁止：自行创建验收标记而不与用户确认"
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
