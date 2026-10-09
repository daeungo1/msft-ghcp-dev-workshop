#!/usr/bin/env bash
# preToolUse 훅 스타터: 입출력과 판정 틀은 완성되어 있습니다. TODO 두 곳의 규칙 목록만 채우세요.
# 채운 뒤 scripts/hooks/test_hooks.sh 로 검사합니다.
#
# 입력(stdin):  {"sessionId", "timestamp", "cwd", "toolName", "toolArgs"}  (toolArgs는 객체 또는 JSON 문자열)
# 출력(stdout): {"permissionDecision": "allow|deny", "permissionDecisionReason": "..."}
#
# preToolUse 명령 훅은 비정상 종료하면 도구 실행이 막힙니다(fail-closed).
# 그래서 스크립트 오류는 allow로 처리하고 사유를 stderr에 남깁니다.
set -uo pipefail

HOOK_INPUT="$(cat)"
export HOOK_INPUT

python3 - <<'PY'
import json
import os
import re
import sys


def emit(decision, reason=None):
    out = {"permissionDecision": decision}
    if reason:
        out["permissionDecisionReason"] = reason
    print(json.dumps(out, ensure_ascii=False))
    sys.exit(0)


SHELL_TOOLS = {"bash", "powershell", "shell", "execute", "run_in_terminal"}
EDIT_TOOLS = {
    "edit", "create", "write", "write_file", "edit_file", "str_replace",
    "str_replace_editor", "multi_edit", "replace_in_file", "apply_patch",
}

# TODO 규칙 1: 파괴적 셸 명령. (정규식, 거부 사유) 쌍을 채웁니다.
# 힌트: rm -rf, git push --force, git reset --hard, DROP TABLE, 원격 스크립트 파이프 실행
DANGEROUS_COMMANDS = [
    # (r"\brm\s+-rf\b", "rm -rf 는 허용되지 않습니다"),
]

# TODO 규칙 2: 편집하면 안 되는 경로. (정규식, 거부 사유) 쌍을 채웁니다.
# 힌트: .env, DB 파일, .git/, 가드레일 설정과 스크립트 자신
PROTECTED_PATHS = [
    # (r"(^|/)\.env(\..*)?$", "환경 변수 파일(.env)은 편집할 수 없습니다"),
]


def as_dict(value):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except ValueError:
            return {"command": value}
    return value if isinstance(value, dict) else {}


def edited_paths(args):
    paths = [str(args[k]) for k in ("path", "file_path", "filePath", "file") if args.get(k)]
    # apply_patch 계열은 패치 본문에 대상 경로가 들어 있습니다
    for text in args.values():
        if isinstance(text, str):
            paths += re.findall(r"^\*\*\* (?:Update|Add|Delete) File: (.+)$", text, re.M)
    return paths


def main():
    event = json.loads(os.environ.get("HOOK_INPUT") or "{}")
    tool = str(event.get("toolName", "")).lower()
    args = as_dict(event.get("toolArgs"))
    root = os.path.realpath(event.get("cwd") or os.getcwd())

    if tool in SHELL_TOOLS:
        command = str(args.get("command") or args.get("cmd") or "")
        for pattern, reason in DANGEROUS_COMMANDS:
            if re.search(pattern, command, re.I):
                emit("deny", reason)

    if tool in EDIT_TOOLS:
        for path in edited_paths(args):
            absolute = os.path.realpath(path if os.path.isabs(path) else os.path.join(root, path))
            if absolute != root and not absolute.startswith(root + os.sep):
                emit("deny", f"저장소 밖 경로는 편집할 수 없습니다: {path}")
            relative = os.path.relpath(absolute, root).replace(os.sep, "/")
            for pattern, reason in PROTECTED_PATHS:
                if re.search(pattern, relative):
                    emit("deny", f"{reason}: {relative}")

    emit("allow")


try:
    main()
except SystemExit:
    raise
except Exception as exc:  # 훅 자체 오류로 전체 작업이 멈추지 않게 합니다
    print(f"pre_tool_guard: ignored internal error: {exc}", file=sys.stderr)
    emit("allow")
PY
