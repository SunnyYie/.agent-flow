#!/usr/bin/env python3
"""
AgentFlow Parallel Execution Enforcer — UserPromptSubmit hook
在每个用户 prompt 提交时，检查当前阶段是否需要并行执行，
并提醒 Agent 按照并行策略执行。

检查逻辑：
1. 读取 current_phase.md 中的当前阶段
2. 根据 agent-flow 铁律判断该阶段是否需要并行
3. 如果需要并行但未检测到并行执行标记，注入提醒

并行场景（agent-flow 铁律第7条）：
| 阶段 | 并行方式 | 原因 |
|------|---------|------|
| 需求规格说明书验收 | 双验收：Verifier Agent + Main Agent | 单视角验收容易遗漏 |
| 写代码 | 多个独立子任务并行 Executor Agent | 无依赖的子任务串行=浪费时间 |
| 代码审查 | code-reviewer Agent 独立审查 | 开发者自己审查有盲区 |
| 测试验收 | Verifier Agent + Main Agent 双验收 | 单一验收=低质量 |
"""
import os
import sys


PARALLEL_MARKER = ".agent-flow/state/.parallel-execution-done"
COMPLEXITY_FILE = ".agent-flow/state/.complexity-level"

# 需要并行的关键词（出现在用户 prompt 或 current_phase.md 中）
VERIFY_KEYWORDS = ["验收", "verify", "VERIFY", "验收通过", "双验收"]
CODE_REVIEW_KEYWORDS = ["代码审查", "code review", "review", "审查代码"]
TEST_KEYWORDS = ["测试验收", "测试通过", "test pass", "验收测试"]

# 并行提醒模板
PARALLEL_REMINDERS = {
    "verify": """
[AgentFlow PARALLEL] 验收阶段必须双验收！
┌──────────────────────────────────────────────────┐
│ 必须启动 Verifier Agent + Main Agent 独立验收    │
│                                                  │
│ Verifier Agent: 启动独立 Agent 审查代码质量      │
│ Main Agent: 你自己独立审查                       │
│ 两者都 PASS 才能继续                             │
│                                                  │
│ 示例: Agent({description: "Verifier验收", ...})   │
└──────────────────────────────────────────────────┘""",
    "code_review": """
[AgentFlow PARALLEL] 代码修改后必须启动 code-reviewer Agent！
┌──────────────────────────────────────────────────┐
│ 开发者自己审查有盲区，必须独立 Agent 审查        │
│                                                  │
│ 启动 code-reviewer Agent:                        │
│ Agent({description: "代码审查",                   │
│        subagent_type: "general-purpose",          │
│        prompt: "按 code-review skill 四柱框架     │
│                 审查以下代码变更..."})             │
└──────────────────────────────────────────────────┘""",
    "implement_parallel": """
[AgentFlow PARALLEL] 多个独立子任务应并行执行！
┌──────────────────────────────────────────────────┐
│ 当前有多个独立子任务，应并行启动 Agent:          │
│                                                  │
│ 方式: 在一条消息中发送多个 Agent tool call        │
│ Agent({description: "子任务1", ...})              │
│ Agent({description: "子任务2", ...})              │
│                                                  │
│ 无依赖的子任务串行=浪费时间                      │
└──────────────────────────────────────────────────┘""",
}


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


def read_current_phase() -> str:
    """读取 current_phase.md 内容"""
    for path in [".agent-flow/state/current_phase.md", ".dev-workflow/state/current_phase.md"]:
        if os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return ""


def has_parallel_marker() -> bool:
    """检查是否已执行并行操作"""
    return os.path.isfile(PARALLEL_MARKER)


def detect_parallel_needs(phase_content: str, complexity: str) -> list:
    """检测当前阶段是否需要并行执行"""
    needs = []
    content_lower = phase_content.lower()

    # 1. 验收阶段 → 双验收
    if any(kw in content_lower for kw in ["验收", "verify", "VERIFY"]):
        needs.append("verify")

    # 2. 代码修改后 → code-review
    if any(kw in content_lower for kw in ["implement", "实现", "开发", "编码"]):
        needs.append("code_review")

    # 3. 多个子任务 → 并行执行
    if "T1" in phase_content and "T2" in phase_content:
        # 检查是否有独立的子任务
        if "独立" in phase_content or "并行" in phase_content or complexity == "complex":
            needs.append("implement_parallel")

    return needs


def main():
    # 只在 agent-flow 项目中生效
    if not os.path.isdir(".agent-flow") and not os.path.isdir(".dev-workflow"):
        sys.exit(0)

    # 只在 pre-flight 完成后执行
    phase_content = read_current_phase()
    if not phase_content:
        sys.exit(0)

    complexity = get_complexity_level()

    # Simple 任务不需要并行
    if complexity == "simple":
        sys.exit(0)

    # 已有并行标记，跳过
    if has_parallel_marker():
        sys.exit(0)

    # 检测并行需求
    needs = detect_parallel_needs(phase_content, complexity)

    if not needs:
        sys.exit(0)

    # 输出提醒
    reminders = []
    for need in needs:
        reminder = PARALLEL_REMINDERS.get(need, "")
        if reminder:
            reminders.append(reminder)

    if reminders:
        print("\n\n".join(reminders))

    sys.exit(0)


if __name__ == "__main__":
    main()
