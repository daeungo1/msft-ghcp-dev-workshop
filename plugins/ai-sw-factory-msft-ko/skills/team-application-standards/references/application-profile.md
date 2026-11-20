---
title: Application Stack and Production Requirements
description: 기존 앱의 규모와 운영 요구사항을 근거로 기술 선택과 검증 계획을 만드는 결정표
---

## 결정 절차

1. Manifest, lock file, domain 경계, tests, 배포 설정을 읽고 현재 상태를 확인합니다.
2. 사용자, 데이터 민감도, 예상 부하, 배포 환경과 운영 담당자를 확인합니다.
3. 아래 각 항목에 결정, 대안, 근거, 검증 방법과 담당자를 기록합니다.
4. 구현할 항목은 수용 기준과 작업에 연결하고, 이번 범위 밖인 항목은
   이유와 재검토 조건을 남깁니다.
5. 확인하지 않은 성능 수치, 보안 적합성, runtime 지원 상태를 추측하지
   않습니다. Production 배포에 필요한 미결정 항목은 release blocker입니다.

이 결과는 기존 `plan.md`의 application profile로 기록합니다. 별도의
framework나 중복 설정 파일을 만들지 않습니다.

## 기술 및 운영 결정표

| 영역 | 결정할 내용 | 검증 증거 |
|---|---|---|
| 사용자와 범위 | 교육용, 내부 업무용, 공개 서비스 구분; 사용자 규모와 핵심 시나리오 | spec의 수용 기준과 비목표 |
| Runtime과 framework | 기존 stack, 지원 lifecycle, 팀 역량, dependency 호환성 | manifest/lock/CI 일치, 공식 지원 문서 확인 날짜 |
| Frontend | SPA/SSR 필요성, SEO, 초기 로딩, 상태와 server data 관리 | build/typecheck, 측정한 loading 성능, 핵심 흐름 tests |
| 인증과 인가 | 신뢰 경계, OIDC 등 identity 연동, session/token 수명, 서버 역할 검사 | 미인증/권한 없음/만료/다른 사용자 자원 접근 tests |
| 데이터 | SQL/비SQL 선택 이유, 동시 쓰기, unique/index, transaction 경계 | 선택한 DB의 통합 tests, 동시 요청과 쿼리 계획 |
| Schema와 복구 | versioned migration, 배포 순서, backup, RPO/RTO, 복원 담당자 | migration 및 실제 복원 연습 결과 |
| API와 통합 | 입력 schema, error code, pagination, 호환성, rate limit, CORS/CSRF 적용 조건 | OpenAPI/contract tests, 경계값과 오류 경로 tests |
| 성능과 규모 | workload, 동시 사용자, 데이터 크기, p95 지연과 error budget | 합의한 수치와 조건으로 실행한 load test |
| 신뢰성 | timeout, bounded retry, backoff, idempotency, 취소와 자원 한도 | 지연/실패/중복 요청 tests, retry 안전성 확인 |
| 관측성과 지원 | user-safe 오류, request ID, 구조화 logs, metrics, alert와 담당자 | 개인정보/secret 비노출 tests, alert 전달 확인 |
| 보안과 설정 | secrets 주입/회전, 최소 권한, TLS, 설정 검증, dependency 위험 | secret scan, dependency scan, 인가 tests |
| 배포와 운영 | hosting 선택, readiness/liveness 필요성, 환경 분리, rollback, CI gates | 재현 가능한 build, smoke test, rollback 연습 |
| UX와 접근성 | loading/empty/error 상태, keyboard, focus, 화면 크기와 언어 | component tests, 핵심 사용자 흐름 E2E, 접근성 확인 |
| 비용과 소유권 | 예상 사용량, 월 예산, 데이터 보존/삭제, 운영 책임 | 비용 추정의 가정, 보존 정책, runbook과 승인 |

모든 항목에 고비용 도구를 추가하는 것이 목표가 아닙니다. 예를 들어
queue가 없으면 message retry 정책은 `N/A`로 기록할 수 있지만, HTTP 외부
호출이 있으면 timeout 정책을 생략할 수 없습니다. 숫자가 필요한 요구사항은
측정 조건과 합의한 threshold까지 명시해야 완료입니다.

## TeamFeed 교육용 기본 profile

| 항목 | 유지할 선택 | Production 검토 조건 |
|---|---|---|
| Backend | FastAPI, SQLAlchemy 2, Python runtime policy | 새 framework로 전환할 근거가 없으면 유지 |
| Frontend | React, TypeScript, Vite SPA | SEO/SSR 요구가 확인될 때만 rendering 방식 재평가 |
| Database | 로컬 실습의 SQLite | 동시 쓰기, 다중 인스턴스, HA/복구 요구를 기준으로 PostgreSQL 등 비교 |
| 인증 | 실습 전용 `X-Member-Id` | 실제 사용자/민감 데이터 전에는 검증된 identity와 서버 인가 설계 필수 |
| Schema | 실습의 `create_all` 초기화 | 운영 schema 변경에는 versioned migration과 배포/복구 계획 필요 |
| 구조 | 도메인별 `routes/service/repository/api` | 복잡한 use case부터 Core/ports를 선택적으로 추출 |
| 테스트 | pytest, Vitest, import-linter, TypeScript build | 배포할 DB의 통합 tests와 핵심 흐름 E2E 추가 |
| 운영 | 로컬 개발 환경 | hosting, secrets, logs/alerts, backup, 예산과 담당자 결정 |

이 표는 실습 앱을 production-ready로 인증하지 않습니다. PostgreSQL,
OIDC, migration 도구나 cloud resource를 이 plugin update만으로 설치하거나
구현하지 않습니다. 신규 앱은 현재 지원되는 dependency version을 확인하고,
기존 앱의 version 변경은 별도 작업과 회귀 검증으로 진행합니다.

## 검증을 배치할 위치

| 계층 | 책임 |
|---|---|
| Skill/plan | 선택 이유와 수용 기준, 미결정 항목을 명시 |
| Pre-tool hook | 빠른 위험 명령 및 보호 경로 검사; 완전한 보안 sandbox가 아님 |
| Post-tool hook | 프로젝트 소유자가 승인한 짧은 검사 실행, 미설정/성공/실패 구분 |
| CI | lock file, typecheck/build, tests, module 경계, 보안 검사 |
| Release/human gate | 실제 client hook 로딩, 운영 환경 smoke, 복원/rollback, 미결정 항목 승인 |

Hook timeout과 실행 빈도를 고려해 전체 tests, load test, 외부 보안 scan은
매 편집마다 돌리지 않습니다. Hook을 끄거나 실행하지 않는 client에서도
CI가 실패를 차단해야 합니다. 정적 검사 통과나 hook 성공만으로 identity,
backup, deployment가 구현됐다고 보고하지 않습니다.

## 공식 참고 자료

* [FastAPI deployment concepts](https://fastapi.tiangolo.com/deployment/concepts/)
* [SQLite의 적합한 사용 조건](https://www.sqlite.org/whentouse.html)
* [SQLAlchemy schema migrations](https://docs.sqlalchemy.org/en/20/core/metadata.html#altering-database-objects-through-migrations)
* [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
* [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)
* [Copilot plugin 구성과 테스트](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)
* [Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)
