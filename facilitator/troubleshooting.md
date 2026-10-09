---
title: 트러블슈팅
description: 워크샵 중 자주 발생하는 문제와 해결 방법
---

| 증상 | 확인할 것 |
|---|---|
| 훅이 동작하지 않음 | VS Code 대신 Copilot CLI 사용, 실행 권한 `chmod +x scripts/hooks/*.sh`, `.github/hooks/guardrails.json`의 `version`이 1인지 |
| 훅 스크립트가 `bad interpreter`로 실패 | Windows에서 줄바꿈이 CRLF로 바뀐 경우, `sed -i 's/\r$//' scripts/hooks/*.sh` |
| MCP 연결 실패 | `TEAMFEED_DB` 경로, `scripts/seed-db.py` 실행 여부, 폴더 신뢰(trust) 허용 여부 |
| `uv sync`가 느림 | Codespaces prebuild 설정 확인 |
| spec-kit 명령이 보이지 않음 | `specify --help`, `specify init --here --force --integration copilot` 재실행, 세션 재시작 |
| 포트 접속 불가 | Ports 탭에서 8000, 5173 포워딩 확인 |
| Copilot CLI 실행 거부 | 조직의 Copilot CLI 정책 허용 여부 |
| CodeQL 결과가 늦음 | 강사 화면의 데모 PR 결과로 설명 |
| 플러그인 수정이 반영되지 않음 | `copilot plugin install ./plugins/teamfeed-harness`를 다시 실행해 캐시 갱신 |
| `verify-step.sh`가 `uv`를 못 찾음 | `uv` 설치 확인, 설치할 수 없으면 `VERIFY_UV_RUN=""`로 현재 Python 환경 사용 |
| 진행이 너무 뒤처짐 | `scripts/checkpoint.sh S<n-1>`로 직전 정답에서 합류 |
