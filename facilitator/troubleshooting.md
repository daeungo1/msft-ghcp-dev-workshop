---
title: 트러블슈팅
description: 워크샵 중 자주 발생하는 문제와 해결 방법
---

| 증상 | 확인할 것 |
|---|---|
| 훅이 동작하지 않음 | VS Code 대신 Copilot CLI 사용, 스크립트 실행 권한 `chmod +x scripts/hooks/*.sh` |
| MCP 연결 실패 | `TEAMFEED_DB` 경로, `scripts/seed-db.py` 실행 여부, GitHub 인증 |
| `uv sync`가 느림 | Codespaces prebuild 설정 확인 |
| spec-kit 명령이 보이지 않음 | `specify --help`, `specify init` 재실행, Copilot Chat 새로고침 |
| 포트 접속 불가 | Ports 탭에서 8000, 5173 포워딩 확인 |
| Copilot CLI 실행 거부 | 조직의 Copilot CLI 정책 허용 여부 |
| CodeQL 결과가 늦음 | 강사 화면의 데모 PR 결과로 설명 |
