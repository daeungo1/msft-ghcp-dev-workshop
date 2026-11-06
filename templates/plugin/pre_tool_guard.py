#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

"""Block destructive commands and edits to protected paths."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SHELL_TOOLS = {"bash", "powershell", "shell", "execute", "run_in_terminal"}
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
DANGEROUS_COMMANDS = (
    (r"\brm\s+-[a-zA-Z]*(rf|fr)\b", "rm -rf is not allowed"),
    (
        r"\b(?:Remove-Item|ri|rm|del|erase|rd|rmdir)\b"
        r"(?=[^\r\n]*\s-r(?:e(?:c(?:u(?:r(?:s(?:e)?)?)?)?)?)?\b)"
        r"(?=[^\r\n]*\s-f(?:o(?:r(?:c(?:e)?)?)?)?\b)",
        "Remove-Item with recursive force is not allowed",
    ),
    (
        r"\b(?:rd|rmdir|del|erase)\b"
        r"(?=[^\r\n]*\s/s\b)"
        r"(?=[^\r\n]*\s/q\b)",
        "recursive forced deletion is not allowed",
    ),
    (
        r"\b(?:Clear-Disk|Format-Volume|Remove-Partition)\b",
        "destructive storage commands are not allowed",
    ),
    (
        r"\bgit\s+push\b.*(--force\b|--force-with-lease|\s-f\b)",
        "force push is not allowed",
    ),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard is not allowed"),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f is not allowed"),
    (
        r"\b(curl|wget)\b[^|;]*\|\s*(ba)?sh\b",
        "piping a remote script to a shell is not allowed",
    ),
    (r"\bDROP\s+(TABLE|DATABASE)\b", "DROP statements are not allowed"),
)
PROTECTED_PATHS = (
    (r"(^|/)\.env(\..*)?$", "environment files cannot be edited"),
    (r"\.(db|sqlite|sqlite3)$", "database files cannot be edited directly"),
    (r"(^|/)\.git/", ".git internals cannot be edited"),
    (r"(^|/)\.github/hooks/", "hook configuration cannot be edited"),
    (r"(^|/)scripts/hooks/", "hook scripts cannot be edited"),
    (
        r"(^|/)\.ai-sw-factory-msft-ko/",
        "project harness validation scripts cannot be edited",
    ),
)


def emit(decision: str | None = None, reason: str | None = None) -> None:
    """Write one hook decision object."""
    output: dict[str, str] = {}
    if decision:
        output["permissionDecision"] = decision
    if reason:
        output["permissionDecisionReason"] = reason
    print(json.dumps(output, ensure_ascii=False))


def as_dict(value: object) -> dict[str, Any]:
    """Normalize tool arguments to a dictionary."""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return {"command": value}
    return value if isinstance(value, dict) else {}


def edited_paths(args: dict[str, Any]) -> list[str]:
    """Extract edited paths from direct arguments and patch bodies."""
    paths = [
        str(args[key])
        for key in ("path", "file_path", "filePath", "file")
        if args.get(key)
    ]
    for text in args.values():
        if isinstance(text, str):
            paths.extend(
                re.findall(
                    r"^\*\*\* (?:Update|Add|Delete) File: (.+)$",
                    text,
                    re.MULTILINE,
                )
            )
    return paths


def run(event: dict[str, Any]) -> tuple[str | None, str | None]:
    """Evaluate one pre-tool hook event."""
    tool = str(event.get("toolName", "")).lower()
    args = as_dict(event.get("toolArgs"))
    root = Path(str(event.get("cwd") or os.getcwd())).resolve()

    if tool in SHELL_TOOLS:
        command = str(args.get("command") or args.get("cmd") or "")
        command = re.sub(r"(?:`|\\)\r?\n\s*", " ", command)
        for pattern, reason in DANGEROUS_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return "deny", reason

    if tool in EDIT_TOOLS:
        for raw_path in edited_paths(args):
            candidate = Path(raw_path)
            absolute = (candidate if candidate.is_absolute() else root / candidate).resolve()
            try:
                relative = absolute.relative_to(root).as_posix()
            except ValueError:
                return "deny", f"path outside the repository cannot be edited: {raw_path}"
            for pattern, reason in PROTECTED_PATHS:
                if re.search(pattern, relative):
                    return "deny", f"{reason}: {relative}"

    return None, None


def main() -> int:
    """Read the event from stdin and emit a decision."""
    try:
        event = json.load(sys.stdin)
        decision, reason = run(event if isinstance(event, dict) else {})
    except Exception:
        decision, reason = None, None
    emit(decision, reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
