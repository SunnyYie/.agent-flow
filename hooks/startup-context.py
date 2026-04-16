#!/usr/bin/env python3
"""Inject a compact startup context into Claude Code sessions."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _find_project_root() -> Path | None:
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".agent-flow").exists() or (parent / ".dev-workflow").exists():
            return parent
        if parent == Path.home():
            break
    return None


def main() -> None:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return

    project_root = _find_project_root()
    if project_root is None or not (project_root / ".agent-flow").exists():
        return

    prompt = _resolve_prompt(payload)
    if not prompt.strip():
        return

    try:
        from agent_flow.core.startup_context import build_startup_context, render_startup_context_reminder

        context = build_startup_context(project_root, prompt)
        reminder = render_startup_context_reminder(project_root, context)
        if reminder.strip():
            print(reminder)
    except Exception:
        return


def _resolve_prompt(payload: dict) -> str:
    prompt = payload.get("prompt", "")
    if isinstance(prompt, str) and prompt.strip():
        return prompt

    event_name = payload.get("hook_event_name", "")
    if event_name == "SessionStart":
        return "session start"

    return ""


if __name__ == "__main__":
    main()
