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
COMPONENT_PATHS = (
    "spec-kit/workflows/teamfeed-delivery/workflow.yml",
    "spec-kit/extensions/teamfeed-quality/extension.yml",
    "spec-kit/extensions/teamfeed-quality/commands/teamfeed.verify.md",
    "spec-kit/bundles/teamfeed-multi-harness/bundle.yml",
    "spec-kit/README.md",
)
LEARNING_PATHS = (
    "README.md",
    "docs/multi-harness-architecture.md",
    "docs/model-routing.md",
    "labs/S0-spec.md",
    "labs/S1-member-post.md",
    "labs/S2-follow.md",
    "labs/S3-feed.md",
    "labs/S4-report.md",
    "labs/S5-package.md",
    "labs/S6-converge.md",
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
    write_file(
        root,
        COMPONENT_PATHS[0],
        'schema_version: "1.0"\nworkflow:\n  id: "teamfeed-delivery"\n'
        '  version: "1.0.0"\nsteps:\n  - command: speckit.specify\n'
        "  - command: speckit.plan\n  - command: speckit.tasks\n"
        "  - command: speckit.implement\n"
        "  - command: speckit.teamfeed-quality.verify\n"
        "  - command: speckit.converge\n",
    )
    write_file(
        root,
        COMPONENT_PATHS[1],
        'schema_version: "1.0"\nextension:\n  id: "teamfeed-quality"\n'
        '  version: "1.0.0"\n',
    )
    write_file(root, COMPONENT_PATHS[2], "---\ndescription: Verify\n---\n")
    write_file(
        root,
        COMPONENT_PATHS[3],
        'schema_version: "1.0"\nbundle:\n  id: "teamfeed-multi-harness"\n'
        '  version: "1.0.0"\nprovides:\n  extensions:\n'
        '    - id: "teamfeed-quality"\n  workflows:\n'
        '    - id: "teamfeed-delivery"\n',
    )
    write_file(
        root,
        COMPONENT_PATHS[4],
        "specify extension add ./spec-kit/extensions/teamfeed-quality "
        "--dev --force\n"
        "specify workflow add ./spec-kit/workflows/teamfeed-delivery --dev\n"
        "specify bundle install "
        "./spec-kit/bundles/teamfeed-multi-harness --offline\n"
        "specify workflow run teamfeed-delivery\n",
    )
    for path in LEARNING_PATHS:
        write_file(root, path, "learning path\n")


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

    def test_missing_component_source_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            (root / COMPONENT_PATHS[0]).unlink()

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn(COMPONENT_PATHS[0], result.stderr)

    def test_invalid_component_version_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                COMPONENT_PATHS[1],
                'schema_version: "1.0"\nextension:\n'
                '  id: "teamfeed-quality"\n  version: "latest"\n',
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("semantic version", result.stderr)

    def test_bundle_tool_objects_return_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                COMPONENT_PATHS[3],
                'schema_version: "1.0"\nbundle:\n'
                '  id: "teamfeed-multi-harness"\n  version: "1.0.0"\n'
                "requires:\n  tools:\n    - name: git\n      required: true\n"
                "provides:\n  extensions:\n"
                '    - id: "teamfeed-quality"\n  workflows:\n'
                '    - id: "teamfeed-delivery"\n',
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires.tools must be a list of strings", result.stderr)

    def test_missing_learning_path_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            (root / "labs" / "S6-converge.md").unlink()

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("labs/S6-converge.md", result.stderr)

    def test_non_idempotent_extension_install_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                COMPONENT_PATHS[4],
                "specify extension add "
                "./spec-kit/extensions/teamfeed-quality --dev\n"
                "specify workflow run teamfeed-delivery\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("extension install must be idempotent", result.stderr)

    def test_workflow_directory_run_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                "README.md",
                "specify workflow run ./spec-kit/workflows/teamfeed-delivery\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("workflow run must use an installed ID", result.stderr)


if __name__ == "__main__":
    unittest.main()
