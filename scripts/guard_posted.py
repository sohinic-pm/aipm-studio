#!/usr/bin/env python3
"""PreToolUse hook: block any agent write or edit inside posted/.

Only Sohini marks a reel as published, by moving its folder into posted/
herself. Claude Code passes the tool call as JSON on stdin. Exit code 2
blocks the call and shows the message on stderr to Claude.
"""
import json
import os
import sys


def main() -> int:
    try:
        call = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0  # not a tool call we understand; don't block

    path = (call.get("tool_input") or {}).get("file_path", "")
    if not path:
        return 0

    project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    posted = os.path.realpath(os.path.join(project, "posted"))
    target = os.path.realpath(path if os.path.isabs(path) else os.path.join(project, path))

    if target == posted or target.startswith(posted + os.sep):
        print(
            "Blocked: posted/ is Sohini's record of what's live. Agents never "
            "write there. Save to drafts/ instead.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
