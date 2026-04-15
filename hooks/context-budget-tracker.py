#!/usr/bin/env python3
"""
AgentFlow Context Budget Tracker — PostToolUse hook
在每次文件读取后，估算消耗的 token 数并更新 flow-context.yaml 中的预算。

估算方法：
- 读取的文件大小 × 0.3（保守估算：混合中英文内容）
- 追加到 context_budget.used
- 根据 used/max 比例更新 status（healthy|warning|critical）
- 当 status 变化时注入提醒

仅在 flow-context.yaml 存在时生效（Phase 2+ 架构）。
"""
import json
import os
import sys

import yaml


FLOW_CONTEXT_FILE = ".agent-flow/state/flow-context.yaml"

# 保守估算：1 byte ≈ 0.3 token（混合中英文）
BYTES_PER_TOKEN = 3.3  # 1/0.3

# 预算阈值
THRESHOLD_WARNING = 0.5
THRESHOLD_CRITICAL = 0.7

# 单次读取上限提醒（超过此大小建议不要在主 Agent 上下文中读取）
LARGE_FILE_THRESHOLD_BYTES = 50000  # ~50KB ≈ ~15K tokens


def find_flow_context_path() -> str | None:
    """查找 flow-context.yaml 路径，兼容 .agent-flow/ 和 .dev-workflow/"""
    for base in [".agent-flow/state", ".dev-workflow/state"]:
        path = os.path.join(base, "flow-context.yaml")
        if os.path.isfile(path):
            return path
    return None


def get_default_flow_context_path() -> str:
    """获取默认的 flow-context.yaml 路径（用于新建）"""
    if os.path.isdir(".dev-workflow"):
        return ".dev-workflow/state/flow-context.yaml"
    return FLOW_CONTEXT_FILE


def estimate_tokens_from_size(file_path: str) -> int:
    """根据文件大小估算 token 数"""
    try:
        size = os.path.getsize(file_path)
        return int(size / BYTES_PER_TOKEN)
    except OSError:
        return 0


def read_flow_context() -> dict | None:
    """读取 flow-context.yaml，兼容 .agent-flow/ 和 .dev-workflow/"""
    path = find_flow_context_path()
    if path is None:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return None


def write_flow_context(context: dict) -> None:
    """写入 flow-context.yaml（原子写入），兼容 .agent-flow/ 和 .dev-workflow/"""
    target_path = find_flow_context_path() or get_default_flow_context_path()
    # 确保目录存在
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    tmp_path = target_path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            yaml.dump(context, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        os.replace(tmp_path, target_path)
    except Exception:
        try:
            with open(target_path, "w", encoding="utf-8") as f:
                yaml.dump(context, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except Exception:
            pass


def compute_status(used: int, max_budget: int) -> str:
    """计算预算状态"""
    if max_budget <= 0:
        return "healthy"
    ratio = used / max_budget
    if ratio >= THRESHOLD_CRITICAL:
        return "critical"
    elif ratio >= THRESHOLD_WARNING:
        return "warning"
    return "healthy"


def main():
    # 全局生效：不再检查 .agent-flow/ 目录
    # 但只在 flow-context.yaml 存在时追踪预算
    context = read_flow_context()
    if context is None:
        sys.exit(0)

    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只追踪读取操作（Read/Bash/Grep/Glob）和写入操作（Write/Edit）
    # 读取会增加上下文，写入也会（因为 Write 的 content 参数在上下文中）
    tracked_tools = {"Read", "Grep", "Glob"}
    if tool_name not in tracked_tools:
        # 对于 Bash，检查是否是 cat/head/tail/type 等读取命令
        if tool_name == "Bash":
            cmd = tool_input.get("command", "")
            read_cmds = ("cat ", "head ", "tail ", "type ", "less ", "more ")
            if not any(cmd.startswith(rc) for rc in read_cmds):
                sys.exit(0)
        else:
            sys.exit(0)

    # 获取文件路径
    file_path = tool_input.get("file_path", "")
    if not file_path:
        # Grep/Glob 没有单一文件路径，估算输出大小
        estimated_tokens = 500  # 搜索结果通常较小
    else:
        # 检查文件是否存在
        if not os.path.isfile(file_path):
            sys.exit(0)

        # 估算 tokens
        estimated_tokens = estimate_tokens_from_size(file_path)

        # 大文件警告
        file_size = os.path.getsize(file_path)
        if file_size > LARGE_FILE_THRESHOLD_BYTES:
            print(f"[AgentFlow BUDGET WARNING] 读取大文件: {os.path.basename(file_path)} "
                  f"({file_size // 1024}KB ≈ {estimated_tokens} tokens)\n"
                  f"建议: 如果是子 Agent 的 L3 结果，改用深度上下文分析师模式而非直接读取。")

    # 更新预算
    budget = context.get("context_budget", {})
    current_used = budget.get("used", 0)
    max_budget = budget.get("max", 200000)
    old_status = budget.get("status", "healthy")

    new_used = current_used + estimated_tokens
    new_status = compute_status(new_used, max_budget)

    # 更新 context
    budget["used"] = new_used
    budget["status"] = new_status
    budget["files_read"] = budget.get("files_read", 0) + 1

    # 保留其他字段
    context["context_budget"] = budget
    write_flow_context(context)

    # 状态变化时注入提醒
    if new_status != old_status:
        if new_status == "warning":
            print(f"[AgentFlow BUDGET] 上下文预算进入 WARNING 区域 "
                  f"({new_used // 1000}K / {max_budget // 1000}K = {new_used * 100 // max_budget}%)\n"
                  f"建议:\n"
                  f"1. 优先派发子 Agent 执行剩余任务\n"
                  f"2. 避免读取大文件，只读 L2 摘要\n"
                  f"3. 淘汰 flow-context.yaml 中最早的 L1 摘要（只保留最近 5 条）")
        elif new_status == "critical":
            print(f"[AgentFlow BUDGET CRITICAL] 上下文预算超过 70%！"
                  f"({new_used // 1000}K / {max_budget // 1000}K = {new_used * 100 // max_budget}%)\n"
                  f"强制措施:\n"
                  f"1. 所有剩余工作必须派发给子 Agent\n"
                  f"2. 主 Agent 只做状态管理，不再读取任何非摘要文件\n"
                  f"3. 立即淘汰 L1 摘要缓存，只保留任务 ID 和 artifact 路径\n"
                  f"参考: ~/.agent-flow/skills/context-budget/handler.md")

    sys.exit(0)


if __name__ == "__main__":
    main()
