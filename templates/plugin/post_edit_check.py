#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

"""Run an optional project-specific validation script after edits."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

EDIT_TOOLS = {
    "edit",
    "create",
    "write",
    "write_file",
    "edit_file",
    "str_replace",
    "str_replace_editor",
    "multi_edit",
    "replace_in_file",
    "apply_patch",
}
TIMEOUT_SECONDS = 120


def output(context: str | None = None) -> dict[str, str]:
    """Create the hook output envelope."""
    return {"additionalContext": context} if context else {}


def run(event: dict[str, Any]) -> dict[str, str]:
    """Run project validation when a successful edit occurred."""
    if str(event.get("toolName", "")).lower() not in EDIT_TOOLS:
        return output()

    tool_result = event.get("toolResult")
    if (
        isinstance(tool_result, dict)
        and str(tool_result.get("resultType", "success")) != "success"
    ):
        return output()

    root = Path(str(event.get("cwd") or os.getcwd())).resolve()
    check_script = root / ".ai-sw-factory-msft-ko" / "post-edit.py"
    if not check_script.is_file():
        return output()

    try:
        completed = subprocess.run(
            [sys.executable, str(check_script)],
            cwd=root,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return output(
            "ai-sw-factory-msft-ko post-edit validation timed out after 120 seconds. "
            "Check the project validation script before reporting completion."
        )
    except OSError as exc:
        return output(f"ai-sw-factory-msft-ko post-edit validation could not run: {exc}")

    if completed.returncode == 0:
        return output()

    combined = (completed.stdout + completed.stderr).strip()
    tail = "\n".join(combined.splitlines()[-40:])
    return output(
        "Project post-edit validation failed. Fix it before reporting completion."
        f"\n\n{tail}"
    )


def main() -> int:
    """Read one hook event and emit one JSON object."""
    try:
        event = json.load(sys.stdin)
        result = run(event if isinstance(event, dict) else {})
    except Exception as exc:
        result = output(f"ai-sw-factory-msft-ko post-edit internal error: {exc}")
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
