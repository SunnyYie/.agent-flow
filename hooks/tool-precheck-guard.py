#!/usr/bin/env python3
"""
AgentFlow Tool Precheck Guard — PreToolUse hook
在外部 CLI 工具执行前，检查 Agent 是否已读过相关 wiki 文档。
如果未读，输出提醒信息（不阻断，exit 0），包含临界知识区对应条目的要点摘要。

配合 tool-precheck skill 和 critical-knowledge skill 使用。
"""
import json
import os
import sys
import time

# 标记文件路径
TOOL_WIKI_READ_MARKER = ".agent-flow/state/.tool-wiki-read"
COMPLEXITY_FILE = ".agent-flow/state/.complexity-level"
CONFIG_FILE = os.path.expanduser("~/.agent-flow/config.yaml")

# Wiki 已读标记有效期：24 小时
MARKER_MAX_AGE = 86400

# 默认需要监控的 critical tools（如果 config.yaml 未配置）
DEFAULT_CRITICAL_TOOLS = ["lark-cli", "glab", "gh", "docker"]


def load_critical_tools() -> list:
    """从 config.yaml 加载 critical_tools 列表"""
    # 简单解析 YAML（不用 pyyaml 依赖）
    if not os.path.isfile(CONFIG_FILE):
        return DEFAULT_CRITICAL_TOOLS
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            in_critical_tools = False
            tools = []
            for line in f:
                stripped = line.strip()
                if stripped.startswith("critical_tools:"):
                    in_critical_tools = True
                    continue
                if in_critical_tools:
                    if stripped.startswith("- "):
                        tool_name = stripped[2:].strip().strip('"').strip("'")
                        tools.append(tool_name)
                    elif not stripped.startswith("#") and stripped and not stripped.startswith("-"):
                        # 离开 critical_tools 部分
                        if not stripped.startswith("  "):
                            break
            return tools if tools else DEFAULT_CRITICAL_TOOLS
    except Exception:
        return DEFAULT_CRITICAL_TOOLS


def extract_tool_from_command(command: str, critical_tools: list) -> str:
    """从 Bash 命令中提取 critical tool 名称"""
    cmd = command.strip()
    for tool in critical_tools:
        if cmd.startswith(tool):
            return tool
    return ""


def has_recent_wiki_read(tool_name: str) -> bool:
    """检查是否有近期的 wiki 已读标记"""
    if not os.path.isfile(TOOL_WIKI_READ_MARKER):
        return False
    try:
        with open(TOOL_WIKI_READ_MARKER, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) >= 2 and parts[0] == tool_name:
                    # 检查时间戳是否在有效期内
                    try:
                        read_time = time.mktime(time.strptime(parts[1], "%Y-%m-%dT%H:%M:%S"))
                        if time.time() - read_time < MARKER_MAX_AGE:
                            return True
                    except (ValueError, OverflowError):
                        pass
    except Exception:
        pass
    return False


def get_critical_knowledge_summary(tool_name: str) -> str:
    """从 Soul.md 临界知识区提取工具摘要"""
    soul_file = os.path.expanduser("~/.agent-flow/souls/main.md")
    # 也检查项目级
    project_soul = ".agent-flow/souls/main.md"

    for soul_path in [project_soul, soul_file]:
        if not os.path.isfile(soul_path):
            continue
        try:
            with open(soul_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 查找临界知识区
            in_critical_zone = False
            in_tool_section = False
            summary_lines = []

            for line in content.split("\n"):
                if "临界知识区" in line and line.strip().startswith("##"):
                    in_critical_zone = True
                    continue
                if in_critical_zone and line.strip().startswith("## ") and "临界知识区" not in line:
                    # 离开临界知识区
                    break
                if in_critical_zone and line.strip().startswith("### TOOL:"):
                    if f"TOOL: {tool_name}" in line:
                        in_tool_section = True
                        summary_lines.append(line.strip())
                        continue
                    else:
                        if in_tool_section:
                            # 到了下一个 TOOL，结束
                            break
                        continue
                if in_tool_section:
                    stripped = line.strip()
                    if stripped:
                        summary_lines.append(stripped)

            if summary_lines:
                return "\n".join(summary_lines)
        except Exception:
            continue
    return ""


def main():
    # 只在 agent-flow 项目中生效
    if not os.path.isdir(".agent-flow") and not os.path.isdir(".dev-workflow"):
        sys.exit(0)

    # 读取 hook 输入
    try:
        input_data = json.loads(sys.stdin.read())
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只拦截 Bash 命令
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")
    if not command:
        sys.exit(0)

    # 加载 critical tools 列表
    critical_tools = load_critical_tools()

    # 提取命令中的工具名
    detected_tool = extract_tool_from_command(command, critical_tools)
    if not detected_tool:
        sys.exit(0)  # 不是 critical tool，放行

    # 检查是否有近期的 wiki 已读标记
    if has_recent_wiki_read(detected_tool):
        sys.exit(0)  # 已读过 wiki，放行

    # 未读 wiki → 提醒（不阻断）
    summary = get_critical_knowledge_summary(detected_tool)

    message = f"[AgentFlow REMINDER] 即将使用 {detected_tool}，但未读取相关 wiki 文档！\n"
    if summary:
        message += f"\n临界知识区要点:\n{summary}\n"
    message += (
        f"\n建议: 读取相关 wiki 文档后再执行，或确认临界知识区要点已理解。\n"
        f"读取后 tool-precheck skill 会自动创建已读标记，后续不再提醒。"
    )

    print(message)
    sys.exit(0)  # 不阻断，只提醒


if __name__ == "__main__":
    main()
