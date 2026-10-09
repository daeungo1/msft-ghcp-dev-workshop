---
title: S0 스타터 프롬프트
description: S0에서 spec-kit 명령에 넣을 입력 예시와 AGENTS.md, copilot-instructions.md 작성 가이드
---

## spec-kit 초기화

```bash
git add -A && git commit -m "chore: before spec-kit init"   # 초기화 전에 변경을 커밋하거나 stash 합니다
specify init --here --force --integration copilot
```

Copilot Chat 또는 Copilot CLI 세션에서 아래 명령을 차례로 실행합니다. 대괄호 안은 `requirements/00-vision.md`의 내용을 붙여 넣습니다.

```text
/speckit-constitution 아래 원칙을 담은 constitution을 작성해줘.
테스트 우선, 패키지 경계(다른 패키지는 api 모듈로만 접근), 작은 변경, 에러 응답 형식 통일, 보안 기본값(인가, 입력 검증) 다섯 가지를 포함하고 각 원칙에 검증 방법을 적어줘.
```

```text
/speckit-specify [requirements/00-vision.md 내용]
```

```text
/speckit-plan 백엔드 FastAPI + SQLAlchemy 2 + SQLite, 프론트엔드 React 18 + Vite + TypeScript. 도메인 패키지는 members, posts, follows, reports로 나눈다.
```

```text
/speckit-tasks
```

이 단계에서는 `/speckit-implement`를 실행하지 않습니다. 구현은 S1부터 기능별로 합니다.

## AGENTS.md에 반드시 들어갈 것

| 항목 | 예시 |
|---|---|
| 개발 명령 | `cd backend && uv run pytest`, `cd frontend && npm test` |
| 작업 원칙 | 가정이 있으면 먼저 말한다, 요청 범위만 수정한다 |
| 디렉터리 안내 | 도메인 패키지별 위치 |

## copilot-instructions.md에 들어갈 것

* 언어와 스타일 (타입 힌트, 함수 길이 등 우리 팀 기준)
* 에러 응답 형식
* 테스트 작성 규칙

핵심은 "분량"이 아니라 "지킬 수 있는 규칙 몇 개"입니다. 길어질수록 지켜지는 비율이 떨어집니다.
