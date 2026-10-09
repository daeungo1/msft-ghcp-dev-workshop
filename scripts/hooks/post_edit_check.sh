#!/usr/bin/env bash
# postToolUse 훅: 파일 편집 직후 경계 검사(import-linter)와 해당 패키지 테스트를 실행하고,
# 실패하면 그 내용을 additionalContext로 에이전트에게 돌려줍니다.
#
# 입력(stdin):  {"toolName", "toolArgs", "toolResult": {"resultType", ...}, "cwd", ...}
# 출력(stdout): {} 또는 {"additionalContext": "..."}
# 오프라인 환경에서는 HOOK_UV_RUN="" 로 실행하면 uv 없이 현재 PATH의 도구를 씁니다.
set -uo pipefail

HOOK_INPUT="$(cat)"
export HOOK_INPUT

python3 - <<'PY'
import json
import os
import re
import shlex
import subprocess
import sys

EDIT_TOOLS = {
    "edit", "create", "write", "write_file", "edit_file", "str_replace",
    "str_replace_editor", "multi_edit", "replace_in_file", "apply_patch",
}
UV_RUN = shlex.split(os.environ.get("HOOK_UV_RUN", "uv run"))
TIMEOUT = 40


def finish(context=None):
    print(json.dumps({"additionalContext": context} if context else {}, ensure_ascii=False))
    sys.exit(0)


def as_dict(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return {}
    return value if isinstance(value, dict) else {}


def run(cmd, cwd):
    try:
        done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 0, f"(skipped: {exc})"
    return done.returncode, (done.stdout + done.stderr).strip()


def main():
    event = json.loads(os.environ.get("HOOK_INPUT") or "{}")
    if str(event.get("toolName", "")).lower() not in EDIT_TOOLS:
        finish()
    if str(as_dict(event.get("toolResult")).get("resultType", "success")) != "success":
        finish()

    root = os.path.realpath(event.get("cwd") or os.getcwd())
    args = as_dict(event.get("toolArgs"))
    paths = [str(args[k]) for k in ("path", "file_path", "filePath", "file") if args.get(k)]

    problems = []
    packages = set()
    for path in paths:
        match = re.search(r"backend/app/([a-z_]+)/", path.replace("\\", "/"))
        if match:
            packages.add(match.group(1))
    if not packages:
        finish()

    backend = os.path.join(root, "backend")
    code, output = run(UV_RUN + ["lint-imports"], backend)
    if code != 0:
        problems.append("import-linter 경계 위반:\n" + "\n".join(output.splitlines()[-25:]))

    for package in sorted(packages):
        if os.path.isdir(os.path.join(backend, "tests", package)):
            code, output = run(UV_RUN + ["pytest", "-q", "-x", f"tests/{package}"], backend)
            if code != 0:
                problems.append(f"tests/{package} 실패:\n" + "\n".join(output.splitlines()[-25:]))

    if problems:
        finish("방금 편집한 파일 때문에 검사가 실패했습니다. 완료로 보고하기 전에 고치세요.\n\n" + "\n\n".join(problems))
    finish()


try:
    main()
except SystemExit:
    raise
except Exception as exc:
    print(f"post_edit_check: ignored internal error: {exc}", file=sys.stderr)
    finish()
PY
