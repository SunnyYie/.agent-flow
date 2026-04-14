#!/usr/bin/env python3
"""
AgentFlow Dev Workflow Enforcer — PreToolUse hook
强制执行4条开发铁律（即使 pre-flight 完成后也必须遵守）：
1. 禁止在 main/master/develop 分支上修改代码文件
2. 禁止没有实施计划文档就修改代码文件
3. 特定操作前提醒搜索 Skill（MR、push 等）
4. 遇到错误禁止自行推测（由 error-search-remind.py 处理）

仅在有 .agent-flow/ 或 .dev-workflow/ 的项目中生效。
仅在 pre-flight 完成后（current_phase.md 存在）才执行检查。
"""
import json
import os
import subprocess
import sys

# ============================================================
# 配置
# ============================================================

PROTECTED_BRANCHES = {"main", "master", "develop"}

# 代码文件扩展名 → 修改这些文件需要检查分支和计划
CODE_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".py", ".rs", ".go", ".java", ".kt",
    ".swift", ".m", ".h", ".c", ".cpp", ".rb", ".php", ".vue", ".svelte",
    ".css", ".scss", ".less", ".html", ".sql", ".graphql",
    ".sh", ".bash", ".zsh",
    ".storyboard", ".xib", ".gradle", ".plist",
}

# 代码文件名（无论扩展名）→ 修改需要检查
CODE_FILENAMES = {
    "package.json", "tsconfig.json", "Makefile", "Dockerfile",
    "Podfile", "Gemfile", "build.gradle", "settings.gradle",
    "app.json", "babel.config.js", "metro.config.js",
}

# 需要先搜索 Skill 的 Bash 命令前缀 → 对应 Skill 名称
SKILL_REQUIRED_COMMANDS = [
    ("glab mr", "gitlab-mr-creation"),
    ("git push origin", "git-workflow + gitlab-mr-creation"),
]

# 实施计划的标记内容 → current_phase.md 中包含任一即视为有计划
PLAN_MARKERS = [
    "## 实施计划", "## Implementation Plan", "## 变更点",
    "## CP", "## 代码修改", "## 代码影响",
]

# 允许写入的路径前缀（不受分支和计划限制）
ALLOWED_PATH_PREFIXES = (".agent-flow", ".dev-workflow", ".claude")

# 深度澄清和设计决策标记文件（v3.0 新增）
REQUIREMENT_CLARIFIED_MARKER = ".agent-flow/state/.requirement-clarified"
DESIGN_CONFIRMED_MARKER = ".agent-flow/state/.design-confirmed"


# ============================================================
# 工具函数
# ============================================================

def is_code_file(file_path: str) -> bool:
    """判断文件是否为代码文件（需要实施计划和分支检查）"""
    # 允许 agent-flow 相关路径
    for prefix in ALLOWED_PATH_PREFIXES:
        if prefix in file_path:
            return False

    # 允许 Markdown 和纯文本（文档类）
    _, ext = os.path.splitext(file_path)
    if ext.lower() in (".md", ".txt", ".rst", ".adoc"):
        return False

    # 检查扩展名
    if ext.lower() in CODE_EXTENSIONS:
        return True

    # 检查文件名
    basename = os.path.basename(file_path)
    if basename in CODE_FILENAMES:
        return True

    # 默认放行（宁可漏检不可误阻）
    return False


def get_git_branch() -> str:
    """获取当前 git 分支名"""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def has_implementation_plan() -> bool:
    """检查是否存在实施计划文档"""
    state_dir = ".agent-flow/state"

    # 检查独立的实施计划文件
    plan_files = [
        "requirement-decomposition.md",
        "implementation-plan.md",
        "code-impact-map.md",
    ]
    for pf in plan_files:
        if os.path.isfile(os.path.join(state_dir, pf)):
            return True

    # 检查 current_phase.md 中是否包含计划章节
    phase_file = os.path.join(state_dir, "current_phase.md")
    if os.path.isfile(phase_file):
        try:
            with open(phase_file, "r", encoding="utf-8") as f:
                content = f.read()
            if any(marker in content for marker in PLAN_MARKERS):
                return True
        except Exception:
            pass

    return False


# ============================================================
# 主逻辑
# ============================================================

def main():
    # 只在 agent-flow 项目中生效
    if not os.path.isdir(".agent-flow") and not os.path.isdir(".dev-workflow"):
        sys.exit(0)

    # 只在 pre-flight 完成后执行（preflight-enforce.py 处理 pre-flight 前的阶段）
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

    # ----------------------------------------------------------
    # 检查 1 & 2: Write/Edit → 分支 + 实施计划
    # ----------------------------------------------------------
    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "")

        if not is_code_file(file_path):
            sys.exit(0)  # 非代码文件，放行

        # 检查 1: Git 分支
        branch = get_git_branch()
        if branch in PROTECTED_BRANCHES:
            print(
                f"[AgentFlow BLOCKED] 当前在 {branch} 分支，禁止直接修改代码文件！\n"
                f"请先创建 feature 分支:\n"
                f"  git pull --rebase\n"
                f"  git checkout -b feat/xxx\n"
                f"目标文件: {file_path}"
            )
            sys.exit(2)

        # 检查 2: 实施计划文档
        if not has_implementation_plan():
            print(
                f"[AgentFlow BLOCKED] 没有实施计划文档，禁止修改代码文件！\n"
                f"请先完成:\n"
                f"  1. 搜索并执行 requirement-decomposition 技能\n"
                f"  2. 创建 .agent-flow/state/requirement-decomposition.md\n"
                f"  3. 或在 current_phase.md 中添加 ## 实施计划 章节\n"
                f"  4. 获得用户确认后才能开始编码\n"
                f"目标文件: {file_path}"
            )
            sys.exit(2)

        # 检查 3: 需求澄清标记（v3.0 新增，软提醒）
        if not os.path.isfile(REQUIREMENT_CLARIFIED_MARKER):
            # 检查是否有 requirement-decomposition.md（旧版兼容）
            req_decomp = ".agent-flow/state/requirement-decomposition.md"
            if os.path.isfile(req_decomp):
                # 有拆解文档但没有澄清标记 → 可能是旧版流程创建的，软提醒
                print(
                    f"[AgentFlow REMINDER] 需求澄清标记(.requirement-clarified)不存在！\n"
                    f"建议：执行 requirement-decomposition 技能的 Phase 3.5 深度澄清，\n"
                    f"确保所有假设和不确定项已与用户确认后再修改代码。\n"
                    f"目标文件: {file_path}"
                )
            else:
                # 没有拆解文档也没有澄清标记 → 强烈建议
                print(
                    f"[AgentFlow REMINDER] 需求澄清标记(.requirement-clarified)不存在！\n"
                    f"强烈建议：执行 requirement-decomposition 技能（含 Phase 3.5 深度澄清），\n"
                    f"确保所有假设和不确定项已与用户确认后再修改代码。\n"
                    f"目标文件: {file_path}"
                )
            # v1: 软提醒不阻断，渐进引入后可升级为硬阻断

        # 检查 4: 设计决策确认标记（v3.0 新增，软提醒）
        if not os.path.isfile(DESIGN_CONFIRMED_MARKER):
            print(
                f"[AgentFlow REMINDER] 设计决策确认标记(.design-confirmed)不存在！\n"
                f"建议：执行 requirement-decomposition 技能的 Phase 5.5 设计决策检查点，\n"
                f"确认修改方式、影响范围、实施策略和回滚方案后再修改代码。\n"
                f"目标文件: {file_path}"
            )
            # v1: 软提醒不阻断，渐进引入后可升级为硬阻断

    # ----------------------------------------------------------
    # 检查 3: Bash → Skill 搜索提醒
    # ----------------------------------------------------------
    elif tool_name == "Bash":
        command = tool_input.get("command", "").strip()

        for cmd_prefix, skill_name in SKILL_REQUIRED_COMMANDS:
            if command.startswith(cmd_prefix):
                # 软提醒（不是阻断，但会显示在 Agent 上下文中）
                print(
                    f"[AgentFlow REMINDER] 检测到 '{cmd_prefix}' 命令！\n"
                    f"请先搜索并读取相关 Skill 再执行:\n"
                    f"  Grep '{skill_name.split()[0]}' ~/.agent-flow/skills/ 和 .agent-flow/skills/\n"
                    f"  找到后严格按 Skill 的 Procedure 执行。\n"
                    f"⚠️ 禁止凭经验猜测操作方式！Wiki 已记录先试错再读 Skill 的 pitfall。"
                )
                sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
