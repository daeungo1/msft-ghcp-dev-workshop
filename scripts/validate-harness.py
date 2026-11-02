#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

"""Validate the repository's required multi-harness layers."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

AGENT_PATHS = (
    ".github/agents/researcher.agent.md",
    ".github/agents/planner.agent.md",
    ".github/agents/test-writer.agent.md",
    ".github/agents/implementer.agent.md",
    ".github/agents/security-reviewer.agent.md",
    ".github/agents/convergence-reviewer.agent.md",
)

REQUIRED_PATHS = AGENT_PATHS + (
    ".github/copilot-instructions.md",
    ".github/instructions/backend.instructions.md",
    ".github/instructions/frontend.instructions.md",
    ".github/instructions/python-tests.instructions.md",
    ".github/skills/tdd/SKILL.md",
    ".github/skills/evidence-research/SKILL.md",
    ".github/skills/convergence-check/SKILL.md",
)


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Validate TeamFeed multi-harness structure.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to validate.",
    )
    return parser


def find_missing_paths(root: Path) -> list[str]:
    """Return required repository-relative paths that do not exist."""
    return [path for path in REQUIRED_PATHS if not (root / path).is_file()]


def read_frontmatter(path: Path) -> dict[str, str]:
    """Read scalar YAML frontmatter fields without external dependencies."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip().strip("\"'")
    return {}


def validate_agents(root: Path) -> list[str]:
    """Validate role identity and model-neutral agent declarations."""
    errors: list[str] = []
    names: dict[str, str] = {}
    for relative_path in AGENT_PATHS:
        path = root / relative_path
        if not path.is_file():
            continue

        fields = read_frontmatter(path)
        name = fields.get("name")
        if not name:
            errors.append(f"{relative_path}: missing frontmatter name")
        elif name in names:
            errors.append(
                f"{relative_path}: duplicate agent name: {name} "
                f"(first declared in {names[name]})",
            )
        else:
            names[name] = relative_path

        if not fields.get("description"):
            errors.append(f"{relative_path}: missing frontmatter description")
        if "model" in fields:
            errors.append(f"{relative_path}: must not require a model")
    return errors


def run(root: Path) -> int:
    """Validate required harness files and report actionable failures."""
    missing_paths = find_missing_paths(root)
    errors = [
        f"missing required harness file: {path}"
        for path in missing_paths
    ]
    errors.extend(validate_agents(root))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return EXIT_FAILURE

    print(f"Harness validation passed: {len(REQUIRED_PATHS)} required files")
    return EXIT_SUCCESS


def main() -> int:
    """Run the command-line validator."""
    args = create_parser().parse_args()
    return run(args.root.resolve())


if __name__ == "__main__":
    sys.exit(main())
