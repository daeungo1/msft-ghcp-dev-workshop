#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

"""Validate the repository's required multi-harness layers."""

from __future__ import annotations

import argparse
import json
import re
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

COMPONENT_MANIFESTS = (
    (
        "spec-kit/workflows/teamfeed-delivery/workflow.yml",
        "workflow",
        "teamfeed-delivery",
    ),
    (
        "spec-kit/extensions/teamfeed-quality/extension.yml",
        "extension",
        "teamfeed-quality",
    ),
    (
        "spec-kit/bundles/teamfeed-multi-harness/bundle.yml",
        "bundle",
        "teamfeed-multi-harness",
    ),
)

COMPONENT_PATHS = tuple(path for path, _, _ in COMPONENT_MANIFESTS) + (
    "spec-kit/extensions/teamfeed-quality/commands/teamfeed.verify.md",
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

PLUGIN_PATHS = (
    "plugins/ai-msft-harness/plugin.json",
    "plugins/ai-msft-harness/README.md",
    ".github/plugin/marketplace.json",
    "plugins/ai-msft-harness/mcp.json",
    "plugins/ai-msft-harness/skills/spec-driven-delivery/SKILL.md",
    "plugins/ai-msft-harness/skills/evidence-research/SKILL.md",
    "plugins/ai-msft-harness/skills/tdd/SKILL.md",
    "plugins/ai-msft-harness/skills/convergence-check/SKILL.md",
    "plugins/ai-msft-harness/skills/pr-description/SKILL.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/researcher.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/planner.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/test-writer.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/implementer.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/security-reviewer.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/agents/convergence-reviewer.agent.md",
    "plugins/ai-msft-harness/com.github.copilot/hooks/hooks.json",
    "plugins/ai-msft-harness/com.github.copilot/hooks/pre_tool_guard.py",
    "plugins/ai-msft-harness/com.github.copilot/hooks/post_edit_check.py",
    "templates/plugin/hooks.json",
    "templates/plugin/pre_tool_guard.py",
    "templates/plugin/post_edit_check.py",
    "templates/plugin/skills/spec-driven-delivery/SKILL.md",
    "templates/plugin/skills/pr-description/SKILL.md",
)

REQUIRED_PATHS = AGENT_PATHS + COMPONENT_PATHS + LEARNING_PATHS + PLUGIN_PATHS + (
    ".github/copilot-instructions.md",
    ".github/instructions/backend.instructions.md",
    ".github/instructions/frontend.instructions.md",
    ".github/instructions/python-tests.instructions.md",
    ".github/skills/tdd/SKILL.md",
    ".github/skills/evidence-research/SKILL.md",
    ".github/skills/convergence-check/SKILL.md",
)

SEMANTIC_VERSION_PATTERN = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$",
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


def read_section_scalars(path: Path, section: str) -> dict[str, str]:
    """Read scalar values from one two-space-indented YAML section."""
    values: dict[str, str] = {}
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith(" ") and line.rstrip() == f"{section}:":
            in_section = True
            continue
        if in_section and line and not line.startswith(" "):
            break
        if in_section and line.startswith("  ") and not line.startswith("    "):
            key, separator, value = line.strip().partition(":")
            if separator:
                values[key] = value.strip().strip("\"'")
    return values


def validate_components(root: Path) -> list[str]:
    """Validate local Spec Kit component identities and versions."""
    errors: list[str] = []
    for relative_path, section, expected_id in COMPONENT_MANIFESTS:
        path = root / relative_path
        if not path.is_file():
            continue

        values = read_section_scalars(path, section)
        if values.get("id") != expected_id:
            errors.append(
                f"{relative_path}: {section}.id must be {expected_id}",
            )
        version = values.get("version", "")
        if not SEMANTIC_VERSION_PATTERN.fullmatch(version):
            errors.append(
                f"{relative_path}: {section}.version must be a semantic version",
            )

    workflow_path = root / COMPONENT_MANIFESTS[0][0]
    if workflow_path.is_file():
        workflow = workflow_path.read_text(encoding="utf-8")
        required_commands = (
            "speckit.specify",
            "speckit.plan",
            "speckit.tasks",
            "speckit.implement",
            "speckit.teamfeed-quality.verify",
            "speckit.converge",
        )
        for command in required_commands:
            if command not in workflow:
                errors.append(
                    f"{COMPONENT_MANIFESTS[0][0]}: missing command {command}",
                )

    bundle_path = root / COMPONENT_MANIFESTS[2][0]
    if bundle_path.is_file():
        bundle = bundle_path.read_text(encoding="utf-8")
        for component_id in ("teamfeed-quality", "teamfeed-delivery"):
            if component_id not in bundle:
                errors.append(
                    f"{COMPONENT_MANIFESTS[2][0]}: missing reference {component_id}",
                )
        if re.search(
            r"(?m)^\s{2}tools:\s*$\n\s{4}-\s+name:",
            bundle,
        ):
            errors.append(
                f"{COMPONENT_MANIFESTS[2][0]}: "
                "requires.tools must be a list of strings",
            )
    return errors


def validate_documented_commands(root: Path) -> list[str]:
    """Validate that copyable Spec Kit commands are repeatable and executable."""
    errors: list[str] = []
    component_guide = root / "spec-kit" / "README.md"
    if component_guide.is_file():
        for line in component_guide.read_text(encoding="utf-8").splitlines():
            if (
                "specify extension add "
                "./spec-kit/extensions/teamfeed-quality" in line
                and "--force" not in line
            ):
                errors.append(
                    "spec-kit/README.md: extension install must be idempotent "
                    "with --force",
                )

    invalid_run = re.compile(
        r"specify workflow run "
        r"\./spec-kit/workflows/teamfeed-delivery(?:\s|\\|$)",
    )
    for relative_path in (
        "README.md",
        "spec-kit/README.md",
        "labs/S6-converge.md",
    ):
        path = root / relative_path
        if path.is_file() and invalid_run.search(path.read_text(encoding="utf-8")):
            errors.append(
                f"{relative_path}: workflow run must use an installed ID "
                "or workflow.yml path",
            )
    for relative_path in (
        ".github/skills/speckit-teamfeed-quality-verify/SKILL.md",
        ".specify/extensions/teamfeed-quality/.specify-dev/extension-skills/"
        "speckit-teamfeed-quality-verify/SKILL.md",
    ):
        path = root / relative_path
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if (
            "python scripts/validate-harness.py" not in content
            or "bash scripts/hooks/test_hooks.sh" not in content
            or ".specify/extensions/teamfeed-quality/scripts/" in content
        ):
            errors.append(
                f"{relative_path}: quality skill must use repository validation scripts"
            )
    return errors


def validate_final_plugin(root: Path) -> list[str]:
    """Validate the distributable plugin and marketplace catalog agree."""
    errors: list[str] = []
    plugin_path = root / "plugins" / "ai-msft-harness" / "plugin.json"
    marketplace_path = root / ".github" / "plugin" / "marketplace.json"
    if not plugin_path.is_file() or not marketplace_path.is_file():
        return errors

    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"plugin or marketplace JSON is invalid: {exc}"]

    if plugin.get("$schema") != (
        "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
    ):
        errors.append("ai-msft-harness plugin must use Agent Plugins 1.0 schema")
    if plugin.get("name") != "ai-msft-harness":
        errors.append("plugin name must be ai-msft-harness")
    plugin_version = str(plugin.get("version", ""))
    if not SEMANTIC_VERSION_PATTERN.fullmatch(plugin_version):
        errors.append("ai-msft-harness version must be a semantic version")

    if marketplace.get("name") != "ai-msft-harness-marketplace":
        errors.append("marketplace name must be ai-msft-harness-marketplace")
    entries = [
        item
        for item in marketplace.get("plugins", [])
        if item.get("name") == "ai-msft-harness"
    ]
    if len(entries) != 1:
        errors.append("marketplace must contain one ai-msft-harness entry")
        return errors

    entry = entries[0]
    if str(entry.get("version", "")) != plugin_version:
        errors.append("marketplace version must match plugin version")
    if entry.get("source") != "./plugins/ai-msft-harness":
        errors.append("marketplace source must be ./plugins/ai-msft-harness")

    hooks_path = (
        root
        / "plugins"
        / "ai-msft-harness"
        / "com.github.copilot"
        / "hooks"
        / "hooks.json"
    )
    template_hooks_path = root / "templates" / "plugin" / "hooks.json"
    if hooks_path.is_file():
        try:
            hook_config = json.loads(hooks_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"plugin hooks.json is invalid: {exc}")
        else:
            events = hook_config.get("hooks", {})
            for event_name in ("preToolUse", "postToolUse"):
                hooks = events.get(event_name, [])
                if not hooks:
                    errors.append(f"plugin hooks must define {event_name}")
                    continue
                for hook in hooks:
                    if not hook.get("bash") or not hook.get("powershell"):
                        errors.append(
                            f"{event_name} hooks must define bash and powershell"
                        )
                    if ".py" not in str(hook.get("bash", "")) or ".py" not in str(
                        hook.get("powershell", "")
                    ):
                        errors.append(
                            f"{event_name} hooks must reference portable Python scripts"
                        )

    if hooks_path.is_file() and template_hooks_path.is_file():
        plugin_hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
        template_hooks = json.loads(template_hooks_path.read_text(encoding="utf-8"))
        if plugin_hooks != template_hooks:
            errors.append("template hooks.json must match final plugin hooks.json")
    for script_name in ("pre_tool_guard.py", "post_edit_check.py"):
        plugin_script = hooks_path.parent / script_name
        template_script = root / "templates" / "plugin" / script_name
        if (
            plugin_script.is_file()
            and template_script.is_file()
            and plugin_script.read_bytes() != template_script.read_bytes()
        ):
            errors.append(
                f"template hook scripts must match final plugin: {script_name}"
            )
    return errors


def run(root: Path) -> int:
    """Validate required harness files and report actionable failures."""
    missing_paths = find_missing_paths(root)
    errors = [
        f"missing required harness file: {path}"
        for path in missing_paths
    ]
    errors.extend(validate_agents(root))
    errors.extend(validate_components(root))
    errors.extend(validate_documented_commands(root))
    errors.extend(validate_final_plugin(root))
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
