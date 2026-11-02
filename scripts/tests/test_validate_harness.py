#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = REPOSITORY_ROOT / "scripts" / "validate-harness.py"
AGENT_PATHS = (
    ".github/agents/researcher.agent.md",
    ".github/agents/planner.agent.md",
    ".github/agents/test-writer.agent.md",
    ".github/agents/implementer.agent.md",
    ".github/agents/security-reviewer.agent.md",
    ".github/agents/convergence-reviewer.agent.md",
)
OTHER_REQUIRED_PATHS = (
    ".github/copilot-instructions.md",
    ".github/instructions/backend.instructions.md",
    ".github/instructions/frontend.instructions.md",
    ".github/instructions/python-tests.instructions.md",
    ".github/skills/tdd/SKILL.md",
    ".github/skills/evidence-research/SKILL.md",
    ".github/skills/convergence-check/SKILL.md",
)


def write_file(root: Path, relative_path: str, content: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_complete_harness(root: Path) -> None:
    for index, path in enumerate(AGENT_PATHS, start=1):
        write_file(
            root,
            path,
            f"---\nname: Agent {index}\ndescription: Agent role {index}\n---\n",
        )
    for path in OTHER_REQUIRED_PATHS:
        write_file(root, path, "required content\n")


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        capture_output=True,
        check=False,
        text=True,
    )


class ValidateHarnessTests(unittest.TestCase):
    def test_missing_required_layers_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = run_validator(Path(directory))

        self.assertEqual(result.returncode, 1)
        self.assertIn(".github/agents/researcher.agent.md", result.stderr)
        self.assertIn(".github/skills/evidence-research/SKILL.md", result.stderr)

    def test_duplicate_agent_names_return_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            for path in AGENT_PATHS[:2]:
                write_file(
                    root,
                    path,
                    "---\nname: Duplicate\ndescription: Role description\n---\n",
                )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate agent name: Duplicate", result.stderr)

    def test_required_model_field_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                AGENT_PATHS[0],
                "---\nname: Researcher\ndescription: Research role\nmodel: hydrafusion\n---\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("must not require a model", result.stderr)

    def test_valid_harness_returns_success(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)

            result = run_validator(root)

        self.assertEqual(result.returncode, 0)
        self.assertIn("Harness validation passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
