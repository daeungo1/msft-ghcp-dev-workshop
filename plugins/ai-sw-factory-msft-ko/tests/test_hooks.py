#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HOOKS_ROOT = PLUGIN_ROOT / "com.github.copilot" / "hooks"


def run_hook(script_name: str, payload: dict[str, object]) -> dict[str, object]:
    result = subprocess.run(
        [sys.executable, str(HOOKS_ROOT / script_name)],
        input=json.dumps(payload),
        capture_output=True,
        check=True,
        text=True,
    )
    return json.loads(result.stdout)


class PluginHookTests(unittest.TestCase):
    def test_pre_tool_hook_denies_destructive_command(self) -> None:
        output = run_hook(
            "pre_tool_guard.py",
            {
                "cwd": str(PLUGIN_ROOT),
                "toolName": "execute",
                "toolArgs": {"command": "git reset --hard HEAD~1"},
            },
        )

        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("git reset --hard", output["permissionDecisionReason"])

    def test_pre_tool_hook_defers_safe_command_to_normal_permissions(self) -> None:
        output = run_hook(
            "pre_tool_guard.py",
            {
                "cwd": str(PLUGIN_ROOT),
                "toolName": "execute",
                "toolArgs": {"command": "git status --short"},
            },
        )

        self.assertEqual(output, {})

    def test_pre_tool_hook_denies_destructive_powershell_command(self) -> None:
        output = run_hook(
            "pre_tool_guard.py",
            {
                "cwd": str(PLUGIN_ROOT),
                "toolName": "powershell",
                "toolArgs": {
                    "command": "Remove-Item -Recurse -Force C:\\repo\\src"
                },
            },
        )

        self.assertEqual(output["permissionDecision"], "deny")
        self.assertIn("Remove-Item", output["permissionDecisionReason"])

    def test_pre_tool_hook_denies_abbreviated_powershell_parameters(self) -> None:
        output = run_hook(
            "pre_tool_guard.py",
            {
                "cwd": str(PLUGIN_ROOT),
                "toolName": "powershell",
                "toolArgs": {
                    "command": "Remove-Item -Rec -Fo C:\\repo\\src"
                },
            },
        )

        self.assertEqual(output["permissionDecision"], "deny")

    def test_pre_tool_hook_denies_multiline_powershell_deletion(self) -> None:
        output = run_hook(
            "pre_tool_guard.py",
            {
                "cwd": str(PLUGIN_ROOT),
                "toolName": "powershell",
                "toolArgs": {
                    "command": "ri `\n-Rec `\n-Fo C:\\repo\\src"
                },
            },
        )

        self.assertEqual(output["permissionDecision"], "deny")

    def test_pre_tool_hook_defers_on_invalid_input(self) -> None:
        result = subprocess.run(
            [sys.executable, str(HOOKS_ROOT / "pre_tool_guard.py")],
            input="{not-json",
            capture_output=True,
            check=True,
            text=True,
        )

        self.assertEqual(json.loads(result.stdout), {})

    def test_post_tool_hook_returns_project_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / ".ai-sw-factory-msft-ko" / "post-edit.py"
            script.parent.mkdir()
            script.write_text(
                "import sys\n"
                "print('project check failed', file=sys.stderr)\n"
                "raise SystemExit(7)\n",
                encoding="utf-8",
            )

            output = run_hook(
                "post_edit_check.py",
                {
                    "cwd": str(root),
                    "toolName": "edit",
                    "toolArgs": {"path": "src/app.py"},
                    "toolResult": {"resultType": "success"},
                },
            )

        self.assertIn("project check failed", output["additionalContext"])

    def test_post_tool_hook_reports_unconfigured_validation_instead_of_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = run_hook(
                "post_edit_check.py",
                {
                    "cwd": directory,
                    "toolName": "edit",
                    "toolResult": {"resultType": "success"},
                },
            )

        self.assertIn("not configured", output["additionalContext"])
        self.assertIn(".ai-sw-factory-msft-ko/post-edit.py", output["additionalContext"])
        self.assertIn("No project checks were run", output["additionalContext"])

    def test_post_tool_hook_reports_only_configured_checks_as_passed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / ".ai-sw-factory-msft-ko" / "post-edit.py"
            script.parent.mkdir()
            script.write_text(
                "from pathlib import Path\n"
                "Path('check-ran').write_text('done', encoding='utf-8')\n",
                encoding="utf-8",
            )

            output = run_hook(
                "post_edit_check.py",
                {
                    "cwd": directory,
                    "toolName": "apply_patch",
                    "toolResult": {"resultType": "success"},
                },
            )

            self.assertTrue((root / "check-ran").is_file())
        self.assertIn("passed", output["additionalContext"])
        self.assertIn("configured checks only", output["additionalContext"])

    def test_post_tool_hook_does_not_run_checks_after_reads_or_failed_edits(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            script = root / ".ai-sw-factory-msft-ko" / "post-edit.py"
            script.parent.mkdir()
            script.write_text(
                "raise SystemExit('validation must not run')\n",
                encoding="utf-8",
            )
            for tool_name, result_type in (("view", "success"), ("edit", "failure")):
                with self.subTest(tool_name=tool_name, result_type=result_type):
                    output = run_hook(
                        "post_edit_check.py",
                        {
                            "cwd": directory,
                            "toolName": tool_name,
                            "toolResult": {"resultType": result_type},
                        },
                    )

                    self.assertEqual(output, {})

    def test_hooks_config_has_platform_specific_commands(self) -> None:
        config = json.loads((HOOKS_ROOT / "hooks.json").read_text(encoding="utf-8"))

        for hook in config["hooks"]["preToolUse"] + config["hooks"]["postToolUse"]:
            self.assertIn("bash", hook)
            self.assertIn("powershell", hook)
            self.assertNotIn(".sh", hook["powershell"])
            self.assertIn("[ -f", hook["bash"])
            self.assertIn("Test-Path -LiteralPath", hook["powershell"])
            self.assertIn("'{}'", hook["bash"])
            self.assertIn("'{}'", hook["powershell"])

    def test_powershell_hook_defers_when_plugin_directory_is_missing(self) -> None:
        if os.name != "nt":
            self.skipTest("PowerShell plugin hook applies on Windows")
        config = json.loads((HOOKS_ROOT / "hooks.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            missing_root = Path(directory) / "removed-plugin"
            env = os.environ.copy()
            env["PLUGIN_ROOT"] = str(missing_root)
            for hook in (
                config["hooks"]["preToolUse"] + config["hooks"]["postToolUse"]
            ):
                result = subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        hook["powershell"],
                    ],
                    input="{}",
                    capture_output=True,
                    check=True,
                    env=env,
                    text=True,
                )
                self.assertEqual(json.loads(result.stdout), {})


if __name__ == "__main__":
    unittest.main()
