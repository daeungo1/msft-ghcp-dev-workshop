#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_marketplace",
    SCRIPTS_DIR / "validate-marketplace.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Unable to load marketplace validator")
VALIDATOR_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR_MODULE
SPEC.loader.exec_module(VALIDATOR_MODULE)
validate_repository = VALIDATOR_MODULE.validate_repository


PLUGIN_NAME = "ai-sw-factory-msft-ko"
MARKETPLACE_NAME = f"{PLUGIN_NAME}-marketplace"


def write_json(root: Path, relative_path: str, value: object) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_text(root: Path, relative_path: str, value: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_valid_repository(root: Path) -> None:
    plugin_root = root / "plugins" / PLUGIN_NAME
    write_json(
        root,
        ".github/plugin/marketplace.json",
        {
            "name": MARKETPLACE_NAME,
            "owner": {"name": "team"},
            "plugins": [
                {
                    "name": PLUGIN_NAME,
                    "description": "Team harness",
                    "version": "2.0.0",
                    "source": f"./plugins/{PLUGIN_NAME}",
                }
            ],
        },
    )
    write_json(
        root,
        f"plugins/{PLUGIN_NAME}/plugin.json",
        {
            "$schema": (
                "https://agent-plugins.org/schemas/1.0.0/"
                "plugin.schema.json"
            ),
            "name": PLUGIN_NAME,
            "version": "2.0.0",
            "description": "Team harness",
            "author": {"name": "team"},
            "license": "MIT",
        },
    )
    write_text(
        root,
        f"plugins/{PLUGIN_NAME}/skills/example/SKILL.md",
        "---\n"
        "name: example\n"
        'description: "Use when: validating a marketplace fixture."\n'
        "---\n\n"
        "# Example\n",
    )
    write_text(
        root,
        f"plugins/{PLUGIN_NAME}/com.github.copilot/agents/reviewer.agent.md",
        "---\n"
        "name: reviewer\n"
        "description: Reviews a fixture.\n"
        'tools: ["read"]\n'
        "---\n",
    )
    write_json(
        root,
        f"plugins/{PLUGIN_NAME}/com.github.copilot/hooks/hooks.json",
        {
            "version": 1,
            "hooks": {
                "preToolUse": [
                    {
                        "type": "command",
                        "bash": (
                            'SCRIPT="${PLUGIN_ROOT}/hooks/check.py"; '
                            'if [ -f "$SCRIPT" ]; then python3 "$SCRIPT"; '
                            "else printf '{}'; fi"
                        ),
                        "powershell": (
                            "$script = Join-Path $env:PLUGIN_ROOT "
                            "'hooks\\check.py'; "
                            "if (Test-Path -LiteralPath $script) "
                            "{ python $script } else { '{}' }"
                        ),
                    }
                ]
            },
        },
    )
    write_text(root, f"plugins/{PLUGIN_NAME}/hooks/check.py", "print('{}')\n")
    write_json(
        root,
        f"plugins/{PLUGIN_NAME}/mcp.json",
        {
            "$schema": (
                "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
            ),
            "mcpServers": {
                "example": {
                    "type": "stdio",
                    "command": "python",
                    "args": ["${PLUGIN_ROOT}/mcp/server.py"],
                    "cwd": "${PLUGIN_ROOT}",
                }
            },
        },
    )
    write_text(root, f"plugins/{PLUGIN_NAME}/mcp/server.py", "print('ok')\n")
    write_text(
        root,
        f"plugins/{PLUGIN_NAME}/README.md",
        "Install ai-sw-factory-msft-ko 2.0.0\n",
    )
    self_check = plugin_root / "tests" / "test_hooks.py"
    self_check.parent.mkdir(parents=True, exist_ok=True)
    self_check.write_text("import unittest\n", encoding="utf-8")


class ValidateMarketplaceTests(unittest.TestCase):
    def test_valid_marketplace_has_no_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)

            errors = validate_repository(root)

        self.assertEqual(errors, [])

    def test_plugin_manifest_rejects_unknown_top_level_field(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)
            path = root / "plugins" / PLUGIN_NAME / "plugin.json"
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["skills"] = "./skills"
            write_json(root, f"plugins/{PLUGIN_NAME}/plugin.json", manifest)

            errors = validate_repository(root)

        self.assertTrue(any("unknown plugin.json field" in error for error in errors))

    def test_marketplace_version_must_match_plugin_version(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)
            path = root / ".github" / "plugin" / "marketplace.json"
            marketplace = json.loads(path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["version"] = "9.9.9"
            write_json(root, ".github/plugin/marketplace.json", marketplace)

            errors = validate_repository(root)

        self.assertTrue(any("version must match" in error for error in errors))

    def test_marketplace_source_cannot_escape_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)
            path = root / ".github" / "plugin" / "marketplace.json"
            marketplace = json.loads(path.read_text(encoding="utf-8"))
            marketplace["plugins"][0]["source"] = "../outside"
            write_json(root, ".github/plugin/marketplace.json", marketplace)

            errors = validate_repository(root)

        self.assertTrue(any("must stay inside repository" in error for error in errors))

    def test_skill_name_must_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)
            path = root / "plugins" / PLUGIN_NAME / "skills" / "example" / "SKILL.md"
            path.write_text(
                "---\n"
                "name: wrong\n"
                'description: "Use when: validating a marketplace fixture."\n'
                "---\n",
                encoding="utf-8",
            )

            errors = validate_repository(root)

        self.assertTrue(any("must match skill directory" in error for error in errors))

    def test_mcp_rejects_reserved_environment_override(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_valid_repository(root)
            path = root / "plugins" / PLUGIN_NAME / "mcp.json"
            mcp = json.loads(path.read_text(encoding="utf-8"))
            mcp["mcpServers"]["example"]["env"] = {"PLUGIN_ROOT": "override"}
            write_json(root, f"plugins/{PLUGIN_NAME}/mcp.json", mcp)

            errors = validate_repository(root)

        self.assertTrue(any("reserved MCP environment" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
