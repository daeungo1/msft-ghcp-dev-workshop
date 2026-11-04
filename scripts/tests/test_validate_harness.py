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
    ".github/skills/speckit-teamfeed-quality-verify/SKILL.md",
    ".specify/extensions/teamfeed-quality/.specify-dev/extension-skills/"
    "speckit-teamfeed-quality-verify/SKILL.md",
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
    "docs/images/plugin-installation.svg",
    "docs/images/integration-wrapper-pattern.svg",
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
    "plugins/ai-msft-harness/skills/team-application-standards/SKILL.md",
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
    "templates/plugin/skills/team-application-standards/SKILL.md",
    "templates/plugin/skills/pr-description/SKILL.md",
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
    quality_skill = (
        "python scripts/validate-harness.py\n"
        "bash scripts/hooks/test_hooks.sh\n"
    )
    write_file(
        root,
        ".github/skills/speckit-teamfeed-quality-verify/SKILL.md",
        quality_skill,
    )
    write_file(
        root,
        ".specify/extensions/teamfeed-quality/.specify-dev/extension-skills/"
        "speckit-teamfeed-quality-verify/SKILL.md",
        quality_skill,
    )
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
    write_file(
        root,
        "README.md",
        "docs/images/plugin-installation.svg\n"
        "copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop\n"
        "copilot plugin install ai-msft-harness@ai-msft-harness-marketplace\n"
        "copilot plugin install "
        "daeungo1/msft-ghcp-dev-workshop:plugins/ai-msft-harness\n"
        "copilot plugin marketplace update ai-msft-harness-marketplace\n"
        "copilot plugin update ai-msft-harness@ai-msft-harness-marketplace\n"
        "copilot plugin uninstall ai-msft-harness@ai-msft-harness-marketplace\n"
        "docs/images/integration-wrapper-pattern.svg\n"
        "hy2219/simplified-sdlc\n"
        "Resource Registry\n"
        "HTTP Adapter\n"
        "MCP Adapter\n"
        "Database Adapter\n",
    )
    write_file(
        root,
        PLUGIN_PATHS[0],
        '{"$schema":"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",'
        '"name":"ai-msft-harness","version":"1.0.0",'
        '"description":"Application development harness"}\n',
    )
    write_file(root, PLUGIN_PATHS[1], "ai-msft-harness plugin guide\n")
    write_file(
        root,
        PLUGIN_PATHS[2],
        '{"name":"ai-msft-harness-marketplace","plugins":['
        '{"name":"ai-msft-harness","version":"1.0.0",'
        '"source":"./plugins/ai-msft-harness"}]}\n',
    )
    for path in PLUGIN_PATHS[3:]:
        write_file(root, path, "plugin component\n")
    team_standards = (
        "Node.js >=22\n"
        "Active LTS\n"
        "Maintenance LTS\n"
        "Python >=3.12\n"
        "Core\n"
        "Application Use Cases\n"
        "Ports\n"
        "Adapters\n"
        "module/service\n"
        "incremental refactoring\n"
        "Resource Registry\n"
        "HTTP Adapter\n"
        "MCP Adapter\n"
        "Database Adapter\n"
        "resource manifest\n"
        "inputSchema\n"
        "outputSchema\n"
    )
    write_file(
        root,
        "plugins/ai-msft-harness/skills/team-application-standards/SKILL.md",
        team_standards,
    )
    write_file(
        root,
        "templates/plugin/skills/team-application-standards/SKILL.md",
        team_standards,
    )
    write_file(
        root,
        "plugins/ai-msft-harness/com.github.copilot/hooks/hooks.json",
        '{"version":1,"hooks":{"preToolUse":[{"type":"command",'
        '"bash":"python3 \\"${PLUGIN_ROOT}/com.github.copilot/hooks/'
        'pre_tool_guard.py\\"","powershell":"python \\"$env:PLUGIN_ROOT'
        '\\\\com.github.copilot\\\\hooks\\\\pre_tool_guard.py\\""}],'
        '"postToolUse":[{"type":"command",'
        '"bash":"python3 \\"${PLUGIN_ROOT}/com.github.copilot/hooks/'
        'post_edit_check.py\\"","powershell":"python \\"$env:PLUGIN_ROOT'
        '\\\\com.github.copilot\\\\hooks\\\\post_edit_check.py\\""}]}}\n',
    )
    write_file(
        root,
        "templates/plugin/hooks.json",
        (root / "plugins/ai-msft-harness/com.github.copilot/hooks/hooks.json")
        .read_text(encoding="utf-8"),
    )
    for script_name in ("pre_tool_guard.py", "post_edit_check.py"):
        write_file(
            root,
            f"templates/plugin/{script_name}",
            (
                root
                / "plugins"
                / "ai-msft-harness"
                / "com.github.copilot"
                / "hooks"
                / script_name
            ).read_text(encoding="utf-8"),
        )


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

    def test_missing_final_plugin_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            (root / "plugins" / "ai-msft-harness" / "plugin.json").unlink()

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("plugins/ai-msft-harness/plugin.json", result.stderr)

    def test_marketplace_plugin_version_mismatch_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                ".github/plugin/marketplace.json",
                '{"name":"ai-msft-harness-marketplace","plugins":['
                '{"name":"ai-msft-harness","version":"2.0.0",'
                '"source":"./plugins/ai-msft-harness"}]}\n',
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("marketplace version must match plugin version", result.stderr)

    def test_plugin_hook_without_powershell_command_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                "plugins/ai-msft-harness/com.github.copilot/hooks/hooks.json",
                '{"version":1,"hooks":{"preToolUse":['
                '{"bash":"python3 pre_tool_guard.py"}],'
                '"postToolUse":[{"bash":"python3 post_edit_check.py"}]}}\n',
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("must define bash and powershell", result.stderr)

    def test_stale_plugin_hook_template_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                "templates/plugin/hooks.json",
                '{"version":1,"hooks":{"preToolUse":['
                '{"bash":"bash pre_tool_guard.sh"}]}}\n',
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("template hooks.json must match", result.stderr)

    def test_stale_plugin_hook_script_template_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                "templates/plugin/pre_tool_guard.py",
                "stale policy\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("template hook scripts must match", result.stderr)

    def test_quality_skill_with_missing_extension_scripts_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                ".github/skills/speckit-teamfeed-quality-verify/SKILL.md",
                "python .specify/extensions/teamfeed-quality/scripts/"
                "validate-harness.py\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("quality skill must use repository validation scripts", result.stderr)

    def test_readme_without_installation_guide_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(root, "README.md", "workshop overview only\n")

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("README must document marketplace", result.stderr)

    def test_readme_without_integration_wrapper_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            readme = (root / "README.md").read_text(encoding="utf-8")
            readme = readme.replace("Resource Registry\n", "")
            write_file(root, "README.md", readme)

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest-driven integration wrapper", result.stderr)

    def test_generic_team_standards_skill_returns_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_complete_harness(root)
            write_file(
                root,
                "plugins/ai-msft-harness/skills/"
                "team-application-standards/SKILL.md",
                "Use clean code and supported runtimes.\n",
            )

            result = run_validator(root)

        self.assertEqual(result.returncode, 1)
        self.assertIn("team standards skill must define concrete runtime", result.stderr)


if __name__ == "__main__":
    unittest.main()
