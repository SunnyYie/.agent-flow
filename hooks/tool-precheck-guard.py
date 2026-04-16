#!/usr/bin/env python3
"""
AgentFlow Tool Precheck Guard — PreToolUse hook (Write|Edit matcher)

Before Write/Edit tool use, enforce the "search before execute" principle.
If the tool is Write or Edit and no search (Grep/Glob/Read) has been done
recently, print a gentle reminder.

This is a REMINDER, not a BLOCKER. It outputs a <system-reminder> block
and always exits 0.

Uses .agent-flow/state/.search-tracker to determine if a recent search
has been performed. Falls back to checking if current_phase.md exists
(as a proxy for pre-flight having been done).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Marker file written by search-tracker.py (PostToolUse hook)
SEARCH_TRACKER_FILE = ".agent-flow/state/.search-tracker"
DEV_WORKFLOW_SEARCH_TRACKER = ".dev-workflow/state/.search-tracker"

# Time window for "recent" search (seconds) — 5 minutes
RECENT_SEARCH_WINDOW = 300


def _find_project_root() -> Path | None:
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".agent-flow").exists() or (parent / ".dev-workflow").exists():
            return parent
        if parent == Path.home():
            break
    return None


def _has_recent_search(project_root: Path) -> bool:
    """Check if a search has been performed recently (within RECENT_SEARCH_WINDOW)."""
    for tracker in [SEARCH_TRACKER_FILE, DEV_WORKFLOW_SEARCH_TRACKER]:
        tracker_path = project_root / tracker
        if not tracker_path.is_file():
            continue
        try:
            content = tracker_path.read_text(encoding="utf-8").strip()
            if not content:
                continue
            # Parse last line with timestamp
            # Format: timestamp=ISO8601 or tool=Grep timestamp=...
            for line in reversed(content.splitlines()):
                line = line.strip()
                if not line:
                    continue
                # Extract timestamp
                for part in line.split():
                    if part.startswith("timestamp="):
                        ts_str = part.split("=", 1)[1]
                        try:
                            # Try ISO format
                            from datetime import datetime
                            ts = datetime.fromisoformat(ts_str).timestamp()
                            if time.time() - ts < RECENT_SEARCH_WINDOW:
                                return True
                        except (ValueError, OSError):
                            pass
                        break
                # Check for epoch timestamp
                for part in line.split():
                    if part.startswith("epoch="):
                        try:
                            ts = float(part.split("=", 1)[1])
                            if time.time() - ts < RECENT_SEARCH_WINDOW:
                                return True
                        except (ValueError, OSError):
                            pass
                        break
        except OSError:
            continue
    return False


def _has_preflight_done(project_root: Path) -> bool:
    """Check if pre-flight has been completed (weaker proxy for 'search done')."""
    for state_dir in [".agent-flow/state", ".dev-workflow/state"]:
        phase_path = project_root / state_dir / "current_phase.md"
        if phase_path.is_file():
            try:
                content = phase_path.read_text(encoding="utf-8").strip()
                if content and len(content) > 20:
                    return True
            except OSError:
                pass
    return False


def main() -> None:
    try:
        input_data = json.loads(sys.stdin.read() or "{}")
    except Exception:
        return

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # Only intercept Write and Edit tools
    if tool_name not in ("Write", "Edit"):
        return

    file_path = tool_input.get("file_path", "")

    # Skip if writing to .agent-flow state files (those are internal operations)
    if file_path and any(
        segment in file_path
        for segment in [".agent-flow/state/", ".dev-workflow/state/"]
    ):
        return

    project_root = _find_project_root()
    if project_root is None:
        return

    # Check if a recent search has been done
    if _has_recent_search(project_root):
        return

    # Even without search tracker, if pre-flight was done, that's acceptable
    # (pre-flight includes search steps)
    if _has_preflight_done(project_root):
        # Still give a gentle reminder if no search in the last 5 minutes
        print(
            "<system-reminder>\n"
            "[AgentFlow REMINDER] About to write/edit without a recent search.\n\n"
            "No Grep/Glob/Read operation has been recorded in the last 5 minutes. "
            "The 'search before execute' principle recommends verifying the current "
            "state of the codebase before making changes.\n\n"
            "Consider:\n"
            "  - Grep for related patterns before editing\n"
            "  - Glob for related files before writing new ones\n"
            "  - Read the target file before editing it\n\n"
            "This is a gentle reminder, not a block. Proceed if you have already "
            "searched in a way not tracked by the search tracker.\n"
            "</system-reminder>"
        )
        return

    # No pre-flight done either — stronger reminder
    print(
        "<system-reminder>\n"
        "[AgentFlow REMINDER] About to write/edit without any prior search.\n\n"
        "No recent search operations detected and no pre-flight check recorded. "
        "The 'search before execute' iron law requires searching for existing "
        "patterns, related code, and potential conflicts before making changes.\n\n"
        "Recommended steps:\n"
        "  1. Search for existing implementations: Grep for related patterns\n"
        "  2. Locate related files: Glob for similar filenames\n"
        "  3. Read target file before editing: Read the file you're about to modify\n"
        "  4. Check Wiki/Skills for relevant knowledge\n\n"
        "This is a reminder, not a block. But skipping search increases the risk "
        "of duplicated code, missed edge cases, and conflicts with existing patterns.\n"
        "</system-reminder>"
    )


if __name__ == "__main__":
    main()
