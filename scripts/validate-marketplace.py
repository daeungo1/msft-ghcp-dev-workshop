#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: MIT

"""Validate the GitHub Copilot marketplace and Agent Plugins packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLUGIN_NAME_PATTERN = re.compile(
    r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$"
)
SEMVER_PATTERN = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?$"
)
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
AUTHOR_FIELDS = {"name", "email", "url"}
MARKETPLACE_PLUGIN_FIELDS = {
    "name",
    "description",
    "version",
    "source",
    "category",
}
STDIO_FIELDS = {"type", "command", "args", "env", "cwd"}
REMOTE_FIELDS = {"type", "url", "headers"}
RESERVED_MCP_ENV = {"PLUGIN_ROOT", "PLUGIN_DATA"}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_ROOT = REPOSITORY_ROOT / ".github" / "plugin" / "schemas"


def load_schema(name: str) -> dict[str, Any]:
    """Load one vendored official Agent Plugins schema."""
    path = SCHEMAS_ROOT / name
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: schema must be an object")
    return value


PLUGIN_SCHEMA_DOCUMENT = load_schema("plugin.schema.json")
MCP_SCHEMA_DOCUMENT = load_schema("mcp.schema.json")


def json_type_matches(value: object, expected: str) -> bool:
    """Return whether a value has the JSON type named by the schema."""
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def resolve_schema_ref(root_schema: dict[str, Any], reference: str) -> dict[str, Any]:
    """Resolve a local JSON Pointer used by the vendored schemas."""
    if not reference.startswith("#/"):
        raise ValueError(f"Only local schema references are supported: {reference}")
    value: object = root_schema
    for token in reference[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or token not in value:
            raise ValueError(f"Unresolvable schema reference: {reference}")
        value = value[token]
    if not isinstance(value, dict):
        raise ValueError(f"Schema reference is not an object: {reference}")
    return value


def schema_issues(
    value: object,
    schema: dict[str, Any],
    root_schema: dict[str, Any],
    location: str = "<root>",
) -> list[str]:
    """Evaluate the JSON Schema subset used by Agent Plugins 1.0 schemas."""
    if "$ref" in schema:
        return schema_issues(
            value,
            resolve_schema_ref(root_schema, str(schema["$ref"])),
            root_schema,
            location,
        )
    if "oneOf" in schema:
        branches = [
            schema_issues(value, branch, root_schema, location)
            for branch in schema["oneOf"]
        ]
        if sum(not branch for branch in branches) != 1:
            return [f"{location}: value must match exactly one allowed schema"]
        return []
    if "not" in schema and not schema_issues(
        value,
        schema["not"],
        root_schema,
        location,
    ):
        return [f"{location}: value matches a forbidden schema"]
    if "const" in schema and value != schema["const"]:
        return [f"{location}: value must equal {schema['const']!r}"]
    if "enum" in schema and value not in schema["enum"]:
        return [f"{location}: value must be one of {schema['enum']!r}"]

    expected_type = schema.get("type")
    if expected_type and not json_type_matches(value, str(expected_type)):
        return [f"{location}: expected JSON type {expected_type}"]

    errors: list[str] = []
    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            errors.append(f"{location}: string is shorter than minLength")
        if "maxLength" in schema and len(value) > int(schema["maxLength"]):
            errors.append(f"{location}: string is longer than maxLength")
        pattern = schema.get("pattern")
        if pattern and re.search(str(pattern), value) is None:
            errors.append(f"{location}: string does not match required pattern")

    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for index, item in enumerate(value):
            errors.extend(
                schema_issues(
                    item,
                    schema["items"],
                    root_schema,
                    f"{location}[{index}]",
                )
            )

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{location}: required property is missing: {key}")
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            item_location = f"{location}.{key}"
            if key in properties:
                errors.extend(
                    schema_issues(
                        item,
                        properties[key],
                        root_schema,
                        item_location,
                    )
                )
            elif additional is False:
                errors.append(f"{location}: additional property is not allowed: {key}")
            elif isinstance(additional, dict):
                errors.extend(
                    schema_issues(item, additional, root_schema, item_location)
                )
        property_names = schema.get("propertyNames")
        if isinstance(property_names, dict):
            for key in value:
                errors.extend(
                    schema_issues(
                        key,
                        property_names,
                        root_schema,
                        f"{location}.<property:{key}>",
                    )
                )
    return errors


def validate_schema(
    value: object,
    schema: dict[str, Any],
    path: Path,
    errors: list[str],
) -> None:
    """Validate a JSON value and report deterministic schema error paths."""
    for issue in schema_issues(value, schema, schema):
        errors.append(f"{path}: schema error: {issue}")


def load_json(path: Path, errors: list[str]) -> Any:
    """Load JSON and report decoding or file errors."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path}: file is missing")
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
    return None


def parse_frontmatter(path: Path, errors: list[str]) -> dict[str, str]:
    """Read scalar frontmatter fields needed by marketplace validation."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        errors.append(f"{path}: cannot read file: {exc}")
        return {}
    if not lines or lines[0].strip() != "---":
        errors.append(f"{path}: missing YAML frontmatter")
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip("\"'")
    errors.append(f"{path}: unclosed YAML frontmatter")
    return values


def resolve_source(root: Path, source: str, errors: list[str]) -> Path | None:
    """Resolve a local marketplace source without allowing path traversal."""
    if source.startswith("../") or source.startswith("..\\") or Path(source).is_absolute():
        errors.append(f"marketplace source must stay inside repository: {source}")
        return None
    if not source.startswith("./"):
        errors.append(f"marketplace source must be repository-relative: {source}")
        return None
    resolved = (root / source).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        errors.append(f"marketplace source must stay inside repository: {source}")
        return None
    if not resolved.is_dir():
        errors.append(f"marketplace source directory does not exist: {source}")
        return None
    return resolved


def validate_plugin_manifest(
    path: Path,
    catalog_entry: dict[str, Any],
    errors: list[str],
) -> dict[str, Any] | None:
    """Validate Agent Plugins 1.0 manifest constraints and catalog identity."""
    manifest = load_json(path, errors)
    if not isinstance(manifest, dict):
        errors.append(f"{path}: plugin manifest must be an object")
        return None
    validate_schema(manifest, PLUGIN_SCHEMA_DOCUMENT, path, errors)

    for field in sorted(set(manifest) - PLUGIN_FIELDS):
        errors.append(f"{path}: unknown plugin.json field: {field}")
    if manifest.get("$schema") != PLUGIN_SCHEMA:
        errors.append(f"{path}: $schema must be {PLUGIN_SCHEMA}")

    name = manifest.get("name")
    if not isinstance(name, str) or not PLUGIN_NAME_PATTERN.fullmatch(name):
        errors.append(f"{path}: invalid Agent Plugin name")
    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version):
        errors.append(f"{path}: version must use semantic versioning")
    description = manifest.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{path}: description must be a non-empty string")

    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            errors.append(f"{path}: author must be an object")
        else:
            for field in sorted(set(author) - AUTHOR_FIELDS):
                errors.append(f"{path}: unknown author field: {field}")
            if not isinstance(author.get("name"), str) or not author["name"].strip():
                errors.append(f"{path}: author.name must be a non-empty string")

    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list)
        or not all(isinstance(item, str) and item for item in keywords)
    ):
        errors.append(f"{path}: keywords must be non-empty strings")
    extensions = manifest.get("extensions")
    if extensions is not None and not isinstance(extensions, dict):
        errors.append(f"{path}: extensions must be an object")

    if catalog_entry.get("name") != name:
        errors.append(f"{path}: marketplace name must match plugin name")
    if catalog_entry.get("version") != version:
        errors.append(f"{path}: marketplace version must match plugin version")
    return manifest


def validate_skills(plugin_root: Path, errors: list[str]) -> int:
    """Validate immediate skill directories and discovery frontmatter."""
    skills_root = plugin_root / "skills"
    if not skills_root.is_dir():
        errors.append(f"{skills_root}: skills directory is missing")
        return 0
    count = 0
    for directory in sorted(skills_root.iterdir()):
        if not directory.is_dir():
            errors.append(f"{directory}: skills root may contain directories only")
            continue
        skill = directory / "SKILL.md"
        if not skill.is_file():
            errors.append(f"{directory}: SKILL.md is missing")
            continue
        count += 1
        frontmatter = parse_frontmatter(skill, errors)
        if frontmatter.get("name") != directory.name:
            errors.append(f"{skill}: name must match skill directory")
        description = frontmatter.get("description", "")
        if not description.startswith("Use when:"):
            errors.append(f"{skill}: description must start with 'Use when:'")
    if count == 0:
        errors.append(f"{skills_root}: at least one skill is required")
    return count


def validate_agents(plugin_root: Path, errors: list[str]) -> int:
    """Validate Copilot-specific custom agents."""
    agents_root = plugin_root / "com.github.copilot" / "agents"
    if not agents_root.is_dir():
        return 0
    count = 0
    names: set[str] = set()
    for agent in sorted(agents_root.glob("*.agent.md")):
        count += 1
        frontmatter = parse_frontmatter(agent, errors)
        name = frontmatter.get("name")
        if not name:
            errors.append(f"{agent}: agent name is required")
        elif name in names:
            errors.append(f"{agent}: duplicate agent name: {name}")
        else:
            names.add(name)
        if not frontmatter.get("description"):
            errors.append(f"{agent}: agent description is required")
    return count


def validate_hooks(plugin_root: Path, errors: list[str]) -> int:
    """Validate Copilot hook configuration and referenced scripts."""
    hooks_path = plugin_root / "com.github.copilot" / "hooks" / "hooks.json"
    if not hooks_path.exists():
        return 0
    config = load_json(hooks_path, errors)
    if not isinstance(config, dict):
        return 0
    if config.get("version") != 1 or not isinstance(config.get("hooks"), dict):
        errors.append(f"{hooks_path}: expected version 1 and hooks object")
        return 0

    count = 0
    for event_name, entries in config["hooks"].items():
        if not isinstance(entries, list):
            errors.append(f"{hooks_path}: {event_name} must be a list")
            continue
        for entry in entries:
            count += 1
            if not isinstance(entry, dict):
                errors.append(f"{hooks_path}: {event_name} entry must be an object")
                continue
            if entry.get("type", "command") != "command":
                errors.append(f"{hooks_path}: only command hooks are supported")
            bash = entry.get("bash")
            powershell = entry.get("powershell")
            if not isinstance(bash, str) or not isinstance(powershell, str):
                errors.append(
                    f"{hooks_path}: {event_name} must define bash and powershell"
                )
                continue
            if "[ -f" not in bash or "printf '{}'" not in bash:
                errors.append(f"{hooks_path}: bash hook needs missing-path fallback")
            if "Test-Path -LiteralPath" not in powershell or "'{}'" not in powershell:
                errors.append(
                    f"{hooks_path}: PowerShell hook needs missing-path fallback"
                )
            for command in (bash, powershell):
                for match in re.findall(
                    r"(?:\$\{PLUGIN_ROOT\}|PLUGIN_ROOT)[/\\]([^\"';]+\.py)",
                    command,
                ):
                    referenced = plugin_root / Path(match.replace("\\", "/"))
                    if not referenced.is_file():
                        errors.append(
                            f"{hooks_path}: referenced hook script is missing: {match}"
                        )
    return count


def validate_mcp(plugin_root: Path, errors: list[str]) -> int:
    """Validate Agent Plugins MCP 1.0 envelope and local file references."""
    path = plugin_root / "mcp.json"
    if not path.exists():
        return 0
    config = load_json(path, errors)
    if not isinstance(config, dict):
        return 0
    validate_schema(config, MCP_SCHEMA_DOCUMENT, path, errors)
    if set(config) - {"$schema", "mcpServers"}:
        errors.append(f"{path}: unknown MCP top-level field")
    if config.get("$schema") != MCP_SCHEMA:
        errors.append(f"{path}: $schema must be {MCP_SCHEMA}")
    servers = config.get("mcpServers")
    if not isinstance(servers, dict):
        errors.append(f"{path}: mcpServers must be an object")
        return 0

    for name, server in servers.items():
        if not isinstance(name, str) or not name:
            errors.append(f"{path}: MCP server names must be non-empty strings")
            continue
        if not isinstance(server, dict):
            errors.append(f"{path}: MCP server {name} must be an object")
            continue
        server_type = server.get("type")
        allowed = STDIO_FIELDS if server_type == "stdio" else REMOTE_FIELDS
        if server_type not in {"stdio", "streamable-http", "sse"}:
            errors.append(f"{path}: MCP server {name} has unsupported type")
            continue
        for field in sorted(set(server) - allowed):
            errors.append(f"{path}: MCP server {name} has unknown field: {field}")
        if server_type == "stdio":
            if not isinstance(server.get("command"), str) or not server["command"]:
                errors.append(f"{path}: stdio server {name} requires command")
            args = server.get("args", [])
            if not isinstance(args, list) or not all(
                isinstance(item, str) for item in args
            ):
                errors.append(f"{path}: stdio server {name} args must be strings")
            env = server.get("env", {})
            if not isinstance(env, dict) or not all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in env.items()
            ):
                errors.append(f"{path}: stdio server {name} env must be strings")
            elif RESERVED_MCP_ENV & set(env):
                errors.append(f"{path}: reserved MCP environment cannot be overridden")
            cwd = server.get("cwd")
            if cwd is not None and (
                not isinstance(cwd, str)
                or not re.match(
                    r"^(?:\./|\$\{PLUGIN_ROOT\}(?:/|$)|"
                    r"\$\{PLUGIN_DATA\}(?:/|$))",
                    cwd,
                )
            ):
                errors.append(f"{path}: stdio server {name} has invalid cwd")
            for argument in args:
                prefix = "${PLUGIN_ROOT}/"
                if argument.startswith(prefix):
                    referenced = plugin_root / argument.removeprefix(prefix)
                    if not referenced.is_file():
                        errors.append(
                            f"{path}: MCP referenced file is missing: {argument}"
                        )
        elif not isinstance(server.get("url"), str) or not server["url"]:
            errors.append(f"{path}: remote MCP server {name} requires url")
    return len(servers)


def validate_plugin(
    root: Path,
    plugin_root: Path,
    catalog_entry: dict[str, Any],
    errors: list[str],
) -> dict[str, int]:
    """Validate one local plugin package."""
    validate_plugin_manifest(plugin_root / "plugin.json", catalog_entry, errors)
    readme = plugin_root / "README.md"
    if not readme.is_file():
        errors.append(f"{readme}: plugin documentation is required")
    tests = plugin_root / "tests"
    if not tests.is_dir() or not any(tests.glob("test_*.py")):
        errors.append(f"{tests}: plugin self-tests are required")
    return {
        "skills": validate_skills(plugin_root, errors),
        "agents": validate_agents(plugin_root, errors),
        "hooks": validate_hooks(plugin_root, errors),
        "mcpServers": validate_mcp(plugin_root, errors),
    }


def validate_repository(root: Path) -> list[str]:
    """Return all model-free marketplace and plugin validation errors."""
    errors: list[str] = []
    marketplace_path = root / ".github" / "plugin" / "marketplace.json"
    marketplace = load_json(marketplace_path, errors)
    if not isinstance(marketplace, dict):
        errors.append(f"{marketplace_path}: marketplace must be an object")
        return errors

    name = marketplace.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append(f"{marketplace_path}: marketplace name must be stable kebab-case")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str):
        errors.append(f"{marketplace_path}: owner.name is required")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append(f"{marketplace_path}: plugins must be a non-empty list")
        return errors

    names: set[str] = set()
    for index, entry in enumerate(plugins):
        label = f"{marketplace_path}: plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in sorted(set(entry) - MARKETPLACE_PLUGIN_FIELDS):
            errors.append(f"{label} has unknown field: {field}")
        plugin_name = entry.get("name")
        if not isinstance(plugin_name, str) or not PLUGIN_NAME_PATTERN.fullmatch(
            plugin_name
        ):
            errors.append(f"{label} has invalid plugin name")
        elif plugin_name in names:
            errors.append(f"{label} has duplicate plugin name: {plugin_name}")
        else:
            names.add(plugin_name)
        if not isinstance(entry.get("description"), str) or not entry[
            "description"
        ].strip():
            errors.append(f"{label} description is required")
        if not isinstance(entry.get("version"), str) or not SEMVER_PATTERN.fullmatch(
            entry["version"]
        ):
            errors.append(f"{label} version must use semantic versioning")
        source = entry.get("source")
        if not isinstance(source, str):
            errors.append(f"{label} source must be a local path string")
            continue
        plugin_root = resolve_source(root, source, errors)
        if plugin_root is not None:
            validate_plugin(root, plugin_root, entry, errors)
    return errors


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(
        description="Validate GitHub Copilot marketplace packages."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main() -> int:
    """Run marketplace validation and print a stable report."""
    args = create_parser().parse_args()
    root = args.root.resolve()
    errors = validate_repository(root)
    if args.as_json:
        print(
            json.dumps(
                {"status": "ok" if not errors else "error", "errors": errors},
                ensure_ascii=False,
                indent=2,
            )
        )
    elif errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
    else:
        print("Marketplace validation passed.")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
