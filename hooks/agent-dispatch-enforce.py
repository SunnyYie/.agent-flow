#!/usr/bin/env python3
"""
AgentFlow Agent Dispatch Enforcer — PreToolUse hook (v2.0)
在 EXECUTE 阶段，检查任务是否应该由子 Agent 执行而非主 Agent。
如果主 Agent 试图直接执行应派发的任务，注入派发提醒。

v2.0 新增：
- 上下文预算状态感知（warning/critical 时加强提醒）
- 三级压缩提示（L1/L2/L3 加载指引）
- 摘要验证提示（Medium/Complex 任务完成后提醒 Verifier 抽检）
"""
import json
import os
import sys

import yaml


FLOW_CONTEXT_FILE = ".agent-flow/state/flow-context.yaml"
COMPLEXITY_FILE = ".agent-flow/state/.complexity-level"
ARTIFACTS_DIR = ".agent-flow/artifacts"


def get_complexity_level() -> str:
    """读取复杂度级别，兼容 .agent-flow/ 和 .dev-workflow/"""
    # 尝试找到复杂度文件
    for base in [".agent-flow/state", ".dev-workflow/state"]:
        path = os.path.join(base, ".complexity-level")
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("level="):
                            level = line.split("=", 1)[1].strip().lower()
                            if level in ("simple", "medium", "complex"):
                                return level
            except Exception:
                pass
    return "medium"  # 默认 Medium（安全起见）


def read_flow_context() -> dict:
    """读取 flow-context.yaml，兼容 .agent-flow/ 和 .dev-workflow/"""
    for base in [".agent-flow/state", ".dev-workflow/state"]:
        path = os.path.join(base, "flow-context.yaml")
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
    return {}


def is_execute_phase(context: dict) -> bool:
    """判断当前是否在 EXECUTE 阶段"""
    phase = context.get("workflow", {}).get("phase", "")
    return phase.upper() == "EXECUTE"


def get_context_budget_status(context: dict) -> str:
    """获取上下文预算状态"""
    return context.get("context_budget", {}).get("status", "healthy")


def get_active_agent_count(context: dict) -> int:
    """获取当前活跃的子 Agent 数量"""
    agents = context.get("agents", [])
    return sum(1 for a in agents if a.get("status") == "running")


def has_pending_tasks(context: dict) -> bool:
    """是否有待执行的任务"""
    tasks = context.get("tasks", [])
    return any(t.get("status") == "pending" for t in tasks)


def count_file_modifications(tool_input: dict) -> int:
    """估算当前操作涉及的文件修改数"""
    file_path = tool_input.get("file_path", "")
    # 简单估算：一次操作 = 1 个文件
    return 1 if file_path else 0


def find_state_file(filename: str) -> str:
    """在 .agent-flow/ 或 .dev-workflow/ 中查找状态文件"""
    for base in [".agent-flow/state", ".dev-workflow/state"]:
        path = os.path.join(base, filename)
        if os.path.isfile(path):
            return path
    return ""


def find_flow_context_path() -> str:
    """查找 flow-context.yaml 路径"""
    for base in [".agent-flow/state", ".dev-workflow/state"]:
        path = os.path.join(base, "flow-context.yaml")
        if os.path.isfile(path):
            return path
    return ""


def find_artifacts_dir() -> str:
    """查找 artifacts 目录"""
    for d in [".agent-flow/artifacts", ".dev-workflow/artifacts"]:
        if os.path.isdir(d):
            return d
    return ".agent-flow/artifacts"  # 默认


def main():
    # 全局生效：不再检查 .agent-flow/ 目录
    # 但仍需要找到状态文件才能判断

    # 读取输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只拦截代码修改操作（Write/Edit），不拦截读取操作
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    # 读取上下文
    context = read_flow_context()
    complexity = get_complexity_level()

    # 不在 EXECUTE 阶段，不干预
    if not is_execute_phase(context):
        sys.exit(0)

    # Simple 任务不需要派发
    if complexity == "simple":
        sys.exit(0)

    # 检查上下文预算
    budget_status = get_context_budget_status(context)

    # 检查是否已有子 Agent 在执行
    active_agents = get_active_agent_count(context)

    # 检查是否已有 flow-context.yaml（新架构启用标志）
    has_flow_context = bool(context)

    # === 派发条件判断 ===
    should_dispatch = False
    reason = ""

    if complexity == "complex":
        should_dispatch = True
        reason = "复杂度 Complex (≥8分)，必须派发子 Agent 执行"
    elif budget_status == "critical":
        should_dispatch = True
        reason = "上下文预算 >70%，强制派发剩余工作给子 Agent"
    elif complexity == "medium" and active_agents == 0 and has_pending_tasks(context):
        # Medium 任务在 EXECUTE 阶段且没有活跃子 Agent 时提醒
        should_dispatch = False  # Medium 不强制，但提醒

    if should_dispatch:
        # 构建预算提示
        budget_hint = ""
        if budget_status == "critical":
            budget_hint = "\n⚠️ 上下文 CRITICAL: 主 Agent 只做状态管理，禁止读取任何非摘要文件！"
        elif budget_status == "warning":
            budget_hint = "\n⚠️ 上下文 WARNING: 优先读取 L2 摘要，避免读取 L3 完整结果。"

        # 构建压缩提示
        compression_hint = ""
        if complexity in ("complex", "medium"):
            compression_hint = "\n📋 子 Agent 完成后必须: L1摘要写flow-context + L2摘要写artifacts + Verifier抽检"

        print(f"""[AgentFlow DISPATCH] 当前任务应由子 Agent 执行，而非主 Agent 直接操作！

原因: {reason}{budget_hint}{compression_hint}

请按 main-agent-dispatch Skill 执行:
1. 更新 .agent-flow/state/flow-context.yaml（任务状态 → in_progress）
2. 创建任务包: .agent-flow/artifacts/task-{{id}}-packet.md
3. 派发子 Agent:

   Agent({{
       description: "executor-{{n}}: {{任务标题}}",
       prompt: "你是执行者 Agent。\\n任务: {{任务描述}}\\n任务包: .agent-flow/artifacts/task-{{id}}-packet.md\\n摘要: .agent-flow/artifacts/task-{{id}}-summary.md",
       subagent_type: "general-purpose"
   }})

4. 子 Agent 完成后: 只读 L2 摘要 → 更新 flow-context.yaml
5. Medium/Complex 任务: 派发 Verifier Agent 抽检验证摘要
   参考: ~/.agent-flow/skills/summary-verifier/handler.md

当前活跃子 Agent: {active_agents}/3""")
        # 不阻断，仅提醒
        sys.exit(0)

    # Medium 任务的软提醒
    if complexity == "medium" and active_agents == 0:
        print(f"""[AgentFlow DISPATCH REMINDER] 当前为 Medium 复杂度任务。
建议派发子 Agent 执行，避免主 Agent 上下文溢出。
参考: ~/.agent-flow/skills/main-agent-dispatch/handler.md""")

    sys.exit(0)


if __name__ == "__main__":
    main()
