# Plan.md — GHCP Harness Hands-on Lab 구축 계획

> 대상: AI-DLC 개발자 워크샵 세션 3 「트렌드 Harness 워크샵 (GHCP 기반)」 핸즈온 180분
> 작성: 2026-10-08 · 덱 v2(공식 자산 중심 Hybrid) 기준 · 이전 REPO-PLAN.md를 대체
> 구축 도구: GitHub Copilot (VS Code agent mode 또는 Copilot CLI)

---

## 0. 이 문서 사용법

### 0.1 Copilot에게 주는 시작 프롬프트

Copilot CLI 또는 VS Code agent mode에서 이 파일을 컨텍스트로 붙이고 시작합니다.

```text
#file:Plan.md 를 읽고 이 저장소를 구축해줘.
- Phase 순서대로 진행하고, 각 Phase가 끝나면 멈춰서 "완료 기준" 체크 결과를 보고해줘.
- Phase 0의 공식 문서 확인 결과(docs/authoring/verified-specs.md)가 이 문서와 다르면 공식 문서를 따르고 차이를 보고해줘.
- 커밋은 Task 단위로, 메시지는 "phaseN: <작업>" 형식으로.
- main 브랜치에는 하네스 파일(.github/copilot-instructions.md, AGENTS.md, .github/agents, .github/skills, .github/hooks)을 절대 만들지 마.
```

- Phase마다 plan 모드(Shift+Tab)로 계획을 먼저 확인하고 실행합니다.
- 문서 작업이 많은 Phase 6은 `/fleet`으로 단계 가이드를 병렬 작성해도 됩니다.

### 0.2 구축 중 지켜야 할 규칙

1. **main은 "하네스 없는 상태"를 유지합니다.**
   - 참가자가 main에서 "하네스 없이 시도"할 때 함정이 재현되어야 합니다.
   - 따라서 main에는 Copilot이 자동으로 읽는 파일(커스텀 인스트럭션, AGENTS.md, 에이전트, 스킬, 훅)을 두지 않습니다.
   - 이 Plan.md 자체도 main에 커밋하지 않고 `authoring` 브랜치에만 둡니다.
2. **정답은 폴더가 아니라 브랜치로 둡니다.**
   - `reference/` 폴더를 main에 두면 Copilot이 워크스페이스에서 정답 코드를 읽어 함정 재현을 망칩니다.
   - 정답 앱과 하네스는 `s0-done` … `s5-done` 브랜치에만 둡니다.
3. **경쟁 제품명과 외부 강의명은 쓰지 않습니다.**
   - 저장소의 모든 문서, 주석, 커밋 메시지에 적용합니다.
   - 트렌드 하네스는 `bp-catalog/README.md`에서 "업계 공통 패턴"의 출처 각주로만 언급합니다.
4. **참가자용 문서는 한국어, 코드와 식별자는 영어**로 작성합니다.
5. **가정이 생기면 `docs/authoring/assumptions.md`에 기록**하고 진행합니다.
   - 공식 문서로 확정할 수 없는 값(훅 입출력 형식, 플러그인 스키마 등)은 `TODO(verify)` 주석을 남깁니다.

---

## 1. 목표와 완료 기준

### 1.1 목표

- 참가자가 **빈 저장소에서 TeamFeed(사내 미니 SNS)를 GitHub Copilot으로 처음부터 만들면서**, 기능 하나마다 그 기능에서 터지는 문제를 막는 하네스를 한 겹씩 붙인다.
- 하네스의 중심은 **GitHub·Microsoft 공식 자산**이다:
  - spec-kit, awesome-copilot, hve-core 원칙
  - Copilot CLI 훅, GitHub Actions, GitHub MCP, CodeQL, Copilot code review, Agent Plugins
- 트렌드 하네스는 설치하지 않고 **패턴만 반영**한다.
- 참가자 결과물: 동작하는 앱 + `.github/` 하네스 자산 + 내 팀 규칙 1개가 들어간 팀 플러그인.

### 1.2 저장소 전체 완료 기준

- [ ] Codespaces 기동 후 10분 이내에 `uv run pytest`, `npm test`, `copilot --version`, `specify --help`가 모두 동작
- [ ] `s0-done` … `s5-done`에서 각각 `scripts/verify-step.sh S<n>`이 통과
- [ ] `final` 브랜치에서 `scripts/verify-step.sh ALL` 통과, 태그 `v1.0` 생성
- [ ] 함정 6개를 main 또는 직전 브랜치에서 하네스 없이 단계별 3회 시도해 재현율을 기록. 재현율이 낮은 단계는 `demo/s<n>-trap` 브랜치 준비
- [ ] 정답 하네스를 적용하면 함정이 모두 막힘
- [ ] 단계 가이드 7개(S0~S5, 회고)와 강사 문서 4종 완성
- [ ] 리허설 1회로 단계별 시간이 계획 ±5분 안에 들어옴

---

## 2. 핸즈온 시간표 (180분)

| 단계 | 시간 | 추가 요건 | 붙이는 하네스 | Microsoft·GitHub 기반 | 업계 공통 패턴 (설치 없음) |
|---|---|---|---|---|---|
| S0 Spec | 25분 | 앱 비전 · MVP | constitution, copilot-instructions.md, AGENTS.md, spec · plan · tasks | spec-kit, hve-core 단계 분리, 커스텀 인스트럭션 | 에이전트 행동 원칙 |
| S1 회원·게시글 | 30분 | 가입, 글 작성·목록, 피드 화면 뼈대 | `tdd` 스킬, `test-writer` · `implementer` 에이전트 | Agent Skills, 커스텀 에이전트, awesome-copilot 에셋 | TDD 강제, 역할 분리 |
| S2 팔로우 | 30분 | 팔로우 · 언팔로우 | import-linter 계약, pre·postToolUse 훅, PR CI | Copilot CLI Hooks, GitHub Actions | 위험 명령 · 범위 밖 편집 차단 |
| S3 피드 | 15분 | 팔로우한 사람 글 모아 보기 | 읽기 전용 SQLite MCP, GitHub MCP | MCP 설정 (템플릿 사전 제공) | 최소 권한 도구 접근 |
| S4 신고 | 35분 | 신고, 관리자 처리 화면 | `security-reviewer` 에이전트, 계획 비평 | CodeQL, Copilot code review, rubber duck | 작성자와 분리된 리뷰 |
| S5 패키징 | 30분 | 다음 프로젝트에서 재사용 | 팀 플러그인 + 내 팀 규칙 1개 | Agent Plugins, `copilot plugin install`, 사내 marketplace | — |
| 회고 · 자가진단 | 15분 | — | 함정 6개 회고표, 자가진단 카드 | — | — |

**시간 절약 원칙**
- 참가자는 하네스의 **내용을 쓰는 데** 시간을 씁니다.
- 다음은 `templates/`에 미리 넣어 두고 복사만 합니다: 워크플로(CI, CodeQL), MCP 설정과 읽기 전용 SQLite MCP 서버, 플러그인 골격, 팀 규칙 템플릿, 자가진단 카드.

---

## 3. 저장소 구조

### 3.1 main 브랜치 (참가자 진입점)

```text
ghcp-harness-workshop/
├── README.md                     # 참가자 진입점: 준비물, 단계 순서, 체크포인트 사용법
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create.sh            # uv, Copilot CLI, spec-kit, 의존성 설치
├── .vscode/
│   └── extensions.json           # GitHub Copilot, Python, ESLint 권장
├── backend/
│   ├── pyproject.toml            # FastAPI, SQLAlchemy, pytest, httpx, import-linter (의존성만)
│   ├── app/__init__.py           # 비어 있음
│   └── tests/__init__.py         # 비어 있음
├── frontend/
│   ├── package.json              # React, Vite, TypeScript, Vitest, Testing Library (의존성만)
│   ├── vite.config.ts            # /api → http://localhost:8000 프록시
│   ├── index.html
│   └── src/main.tsx              # "TeamFeed" 제목만 렌더링
├── requirements/                 # 단계별 요건 + 수용 기준 (Given/When/Then)
│   ├── 00-vision.md
│   ├── 01-member-post.md
│   ├── 02-follow.md
│   ├── 03-feed.md
│   ├── 04-report.md
│   └── 05-package.md
├── labs/                         # 단계 가이드 (한국어)
│   ├── S0-spec.md
│   ├── S1-member-post.md
│   ├── S2-follow.md
│   ├── S3-feed.md
│   ├── S4-report.md
│   ├── S5-package.md
│   └── 99-retro.md
├── bp-catalog/
│   └── README.md                 # 업계 공통 패턴 → 우리 BP → GHCP 기능 매핑
├── templates/                    # 사전 제공 자산 (참가자가 복사해서 사용)
│   ├── workflows/ci.yml
│   ├── workflows/codeql.yml
│   ├── mcp/vscode-mcp.json
│   ├── mcp/copilot-cli-mcp-config.json
│   ├── mcp/sqlite-ro-server/     # 읽기 전용 SQLite MCP 서버 (Python, 약 80줄)
│   ├── plugin/plugin.json        # 플러그인 골격
│   ├── team-rule-template.md
│   └── self-check-card.md
├── scripts/
│   ├── verify-step.sh            # 단계별 자동 확인
│   ├── checkpoint.sh             # 늦은 참가자용: sN-done 상태로 이동
│   └── seed-db.py                # S3용 샘플 데이터 (회원 20, 글 200, 팔로우 60)
└── facilitator/
    ├── run-of-show.md
    ├── prerequisites-checklist.md
    ├── troubleshooting.md
    └── trap-log.md               # 함정 재현 시도 기록
```

> main에 **없어야** 하는 것: `.github/copilot-instructions.md`, `AGENTS.md`, `.github/agents/`, `.github/skills/`, `.github/hooks/`, `.github/instructions/`, `.github/workflows/`(템플릿은 `templates/`에), 앱 구현 코드, `Plan.md`.

### 3.2 브랜치 전략

| 브랜치 | 내용 |
|---|---|
| `main` | 3.1 상태. 참가자는 "Use this template"로 각자 저장소를 만들 때 **Include all branches**를 체크 |
| `s0-done` … `s5-done` | 해당 단계 완료 시점의 정답 앱 + 누적 하네스. `s(n)-done`은 `s(n-1)-done`에서 분기 |
| `final` | **모든 단계가 끝난 최종 완성본.** 아래 3.3 참고. 태그 `v1.0` |
| `demo/s1-trap` … `demo/s4-trap` | 함정 재현율이 낮을 때 강사가 보여줄 "하네스 없이 만든 결과" (Phase 5에서 필요한 것만) |
| `authoring` | Plan.md, `docs/authoring/` (verified-specs, assumptions, 리허설 기록) |

`scripts/checkpoint.sh S2` 동작 순서:
1. 로컬 변경을 stash 합니다.
2. `upstream` remote가 없으면 템플릿 원본을 등록합니다.
3. `s2-done`을 fetch 해 `work/s2`로 체크아웃합니다.

Include all branches를 빠뜨린 참가자도 이 스크립트로 합류할 수 있습니다.

### 3.3 `final` 브랜치 (최종 완성본)

`s5-done`에서 분기하고, 참가자 실습 결과를 넘어 "완성된 모습"을 보여 주는 것까지 담습니다.

- **들어가는 것 (s5-done에 추가)**
  - 회고 결과물이 채워진 상태
    - 회고표: `labs/99-retro.md` 정답 열
    - 자가진단 카드 예시 1장
  - 내 팀 규칙 예시 2~3개
    - 예: API 응답 시간 로깅 규칙, 마이그레이션 금지 규칙
    - 플러그인 `v1.0.0`에 포함
  - 사내 marketplace 등록까지 끝난 플러그인
    - 별도 저장소 또는 `marketplace/` 폴더
    - 등록 방법 README 포함
  - 완성 README
    - 화면 캡처: 피드 화면, 신고 관리 화면
    - 하네스 전체 구조도, 단계별 하네스 목록
    - 함정 6개가 막히는 장면 요약
  - 모든 하네스가 켜진 상태의 PR 1건 (Pull request 이력)
    - CI, CodeQL, Copilot code review 결과가 남아 있음
- **용도**
  - 강사: 리허설, 데모, 질문 대응 시 "다 끝나면 이렇게 된다"를 보여 주는 기준
  - 참가자: 워크샵 후 복습, 자기 팀 저장소에 하네스를 옮길 때 참고본
  - 고객 리드 · Inno Hub: 워크샵 결과물 소개, 다음 단계 진단의 출발 자산
- **검증:** `scripts/verify-step.sh ALL`이 S0~S5 항목을 모두 누적 검사해 통과해야 합니다.

---

## 4. TeamFeed 앱 명세 (s5-done 완성 기준)

### 4.1 기술 스택과 실행

- **백엔드:**
  - Python 3.12, FastAPI, SQLAlchemy 2.x, SQLite(`backend/teamfeed.db`)
  - 시작 시 `create_all`로 테이블 생성, 마이그레이션 도구는 쓰지 않음
  - 테스트는 pytest + httpx TestClient, 테스트마다 임시 DB 사용
- **프론트엔드:**
  - React 18 + Vite + TypeScript, 테스트는 Vitest + Testing Library
  - UI 라이브러리·상태 관리 라이브러리는 쓰지 않음
- **실행:**
  - 백엔드: `cd backend && uv run fastapi dev app/main.py` (포트 8000)
  - 프론트엔드: `cd frontend && npm run dev` (포트 5173, `/api` 프록시)
- **크기 목표:** 완성 시 백엔드 + 프론트엔드 합계 2,000 LOC 이하

### 4.2 패키지 경계 (S0 constitution에 명시, S2에서 강제)

```text
backend/app/
├── main.py            # FastAPI 앱, 라우터 등록
├── core/              # db 세션, 설정, current_member 의존성, 공통 오류
├── members/           # api.py · models.py · repository.py · router.py · schemas.py
├── posts/
├── follows/
├── feed/
└── reports/
```

- 다른 패키지에서는 **`app.<pkg>.api`만 import**할 수 있습니다.
- `repository`, `models`는 자기 패키지 안에서만 씁니다.
- `core`는 모든 패키지가 import할 수 있지만, `core`는 도메인 패키지를 import하지 않습니다.

### 4.3 인증 · 인가 (프레임워크 없이 코드에 드러나게)

- 요청 헤더 `X-Member-Id` → `core.auth.current_member` 의존성이 회원을 조회합니다.
  - 헤더가 없거나 회원이 없으면 401입니다.
- 회원 속성 `role`: `MEMBER` | `ADMIN`
- `core.auth.require_admin` 의존성: ADMIN이 아니면 403

### 4.4 API

| 단계 | 메서드 · 경로 | 설명 | 규칙 |
|---|---|---|---|
| S1 | `POST /api/members` | 가입 `{name}` | name 1~30자, 중복 시 409 |
| S1 | `GET /api/members` | 회원 목록 (화면의 회원 선택용) | |
| S1 | `POST /api/posts` | 글 작성 `{content}` | 인증 필요, 1~280자 |
| S1 | `GET /api/posts?author_id=` | 작성자별 글 목록 | 최신순 |
| S2 | `POST /api/follows/{target_id}` | 팔로우 | 자기 자신 400, 중복 409, 대상 없음 404 |
| S2 | `DELETE /api/follows/{target_id}` | 언팔로우 | 없으면 404 |
| S2 | `GET /api/members/{id}/following` | 팔로잉 목록 | |
| S3 | `GET /api/feed?limit=20&before=` | 팔로우한 사람 + 본인 글, 최신순 | 숨김 글 제외, 커서 페이지네이션 |
| S4 | `POST /api/posts/{id}/reports` | 신고 `{reason}` | 같은 사람이 같은 글 중복 신고 409 |
| S4 | `GET /api/reports?status=OPEN&q=` | 신고 목록 (관리자) | `require_admin`, `q`는 reason 키워드 검색 |
| S4 | `PATCH /api/reports/{id}` | 처리 `{status: ACCEPTED \| REJECTED}` | `require_admin`, ACCEPTED면 글 숨김 |

### 4.5 화면

1. **피드 화면 (S1 뼈대 → S3 완성)**
   - 상단 회원 선택 드롭다운이 `X-Member-Id`를 설정합니다.
   - 글쓰기 폼, 피드 목록, 작성자 옆 팔로우·언팔로우 버튼, 글별 신고 버튼(S4)이 있습니다.
2. **신고 관리 화면 (S4)**
   - ADMIN 회원 선택 시에만 탭이 보입니다.
   - OPEN 신고 목록, 키워드 검색, 승인·반려 버튼이 있습니다.

---

## 5. 요건 속 함정

함정은 "하네스 없이 시키면 재현되고, 하네스를 붙이면 막히는 것"이어야 합니다. 요건 문서는 기능만 담담하게 쓰고, 함정을 피하는 힌트를 넣지 않습니다.

| 단계 | 함정 | 재현을 돕는 장치 | 막는 하네스 | 통제 방식 |
|---|---|---|---|---|
| S0 | 프롬프트마다 패키지 구조 · 네이밍 · 응답 형식이 달라짐 | 가이드에서 같은 기능을 두 번 다른 문장으로 요청하게 함 | constitution, copilot-instructions.md, AGENTS.md | 안내 |
| S1 | 테스트 없이 "완료" 보고, 실패 테스트를 고쳐서 통과시킴 | 가이드 프롬프트: "회원·게시글 기능 만들고 테스트 다 통과시켜줘" | `tdd` 스킬, `test-writer`·`implementer` 분리, 테스트 수정 금지 규칙 | 안내 + 역할 분리 |
| S2 | `follows`가 `members.repository`를 직접 import | `members/repository.py`에 `get_by_id`가 있고, `members/api.py`에는 해당 함수가 아직 없음 (S1 정답에서 의도적으로 빼 둠) | import-linter 계약 + postToolUse 훅 + PR CI | 강제 |
| S3 | 테이블 · 컬럼 이름을 추측한 쿼리, DB 직접 수정 시도 | S1~S2 정답의 컬럼명이 일반적이지 않음 (`posts.body`, `posts.created_ts`, `follows.follower_member_id`) | 읽기 전용 SQLite MCP (스키마 조회 도구 제공, SELECT만 허용) | 도구 범위 제한 |
| S4 | 상태 변경 API에 `require_admin` 누락, 테스트는 통과 | 테스트 픽스처 기본 클라이언트가 ADMIN 회원으로 요청 | `security-reviewer` (인가 누락 = Critical), rubber duck | 독립 리뷰 |
| S4 보조 | 키워드 검색을 f-string SQL로 작성 (SQL 인젝션) | 요건에 "LIKE 검색 · 부분 일치"를 명시 | CodeQL 코드 스캐닝 | 결정적 스캔 |
| S5 | 하네스가 이 저장소에만 존재 | — | 팀 플러그인 + 사내 marketplace | 배포 |

> CodeQL은 인젝션 같은 **알려진 취약 패턴**을 잡고, 인가 누락 같은 **비즈니스 로직 결함**은 리뷰어 에이전트가 맡습니다. 이 역할 구분을 S4 가이드와 회고에서 명확히 설명합니다.

---

## 6. 단계별 상세 설계

모든 단계 가이드(`labs/S*.md`)는 같은 형식을 따릅니다.

```text
# S<n> <제목> (<시간>분)
## 목표 (한 줄)
## 추가 요건            → requirements/0n-*.md 링크와 요약
## 1. 하네스 없이 시도   → 복사해 쓰는 프롬프트
## 2. 관찰              → 체크 포인트 2~3개
## 3. 하네스 추가        → 만들 파일, 들어갈 내용, Copilot에게 시킬 프롬프트
## 4. 같은 요청 재실행   → 1번 프롬프트 그대로
## 5. 완료 확인          → scripts/verify-step.sh S<n>
## 막히면               → scripts/checkpoint.sh S<n-1> / 자주 나는 오류
## 업계 공통 패턴        → bp-catalog 링크 한 줄
```

### S0 Spec (25분)

- **목표:** 앱의 원칙과 범위를 먼저 정해, 이후 모든 요청의 구조·스타일을 고정한다.
- **진행 (분)**
  - 3 — 하네스 없이 "회원 가입 API 만들어줘"를 두 번 다른 문장으로 요청 → 구조 차이 확인 → 변경 버리기 (`git restore . && git clean -fd`)
  - 4 — `specify init --here --integration copilot` (TODO(verify): `--here` 지원 여부, 생성 파일 위치)
  - 8 — `/speckit-constitution`으로 우리 BP 작성
  - 7 — `/speckit-specify` → `/speckit-plan` → `/speckit-tasks`로 MVP 범위 정의 (구현은 S1부터)
  - 3 — `copilot-instructions.md`, `AGENTS.md` 작성 후 같은 요청 재실행해 구조 일치 확인
- **constitution에 반드시 들어갈 우리 BP (최소 5개)**
  1. 패키지 경계: 다른 패키지는 `app.<pkg>.api`만 import
  2. 테스트 먼저: 구현 커밋 전에 실패하는 테스트 커밋
  3. 인가: 상태를 바꾸는 API는 인가 의존성을 명시하고 테스트로 403을 확인
  4. DB 접근: 스키마는 추측하지 말고 도구로 확인, 쓰기는 repository를 통해서만
  5. 범위: 요청 범위 밖 파일은 수정하지 않고, 필요하면 먼저 제안
  6. 응답 형식: 오류는 `{"error": {"code", "message"}}`
- **산출물 (s0-done):**
  - `.specify/memory/constitution.md` (TODO(verify): spec-kit 저장 위치)
  - `specs/001-teamfeed-mvp/{spec,plan,tasks}.md`
  - `.github/copilot-instructions.md`: 스택, 실행·테스트 명령, 패키지 경계 요약, 코드 스타일
  - `AGENTS.md`: 에이전트 행동 원칙 4개(가정은 말하고 시작, 가장 단순한 해법, 요청 범위만 수정, 검증 기준 먼저)와 테스트 명령
- **verify:** 위 파일 존재, constitution의 원칙 항목 5개 이상, `AGENTS.md`에 테스트 명령 포함

### S1 회원·게시글 (30분)

- **목표:** 테스트가 구현보다 먼저 오고, 구현자가 테스트를 바꾸지 못하게 한다.
- **진행 (분)**
  - 5 — 하네스 없이 "회원·게시글 기능 만들고 테스트 다 통과시켜줘" → 테스트 누락, 또는 테스트를 구현에 맞춰 고친 흔적 관찰 → 버리기
  - 4 — awesome-copilot에서 TDD 관련 에이전트·스킬을 찾아보고 출발점으로 복사 (TODO(verify): Phase 0에서 실제 에셋 이름 확정, 없으면 `templates/`에 출발점 제공)
  - 8 — `.github/skills/tdd/SKILL.md` 작성
  - 5 — `test-writer`, `implementer` 커스텀 에이전트 작성
  - 8 — test-writer로 테스트 작성·커밋 → implementer로 구현·커밋, 피드 화면 뼈대 (회원 선택 + 글 목록 + 글쓰기)
- **파일**
  - `.github/skills/tdd/SKILL.md`
    - frontmatter: `name: tdd`, `description: 기능 구현 요청 시 실패하는 테스트부터 작성하는 절차`
    - 본문: RED → GREEN → REFACTOR 절차, 테스트 위치 규칙(`backend/tests/<pkg>/test_*.py`), 커밋 순서, "테스트를 통과시키려고 테스트를 수정하지 않는다"
  - `.github/agents/test-writer.agent.md`
    - 역할: requirements의 Given/When/Then을 pytest로 옮김
    - 수정 범위: `backend/tests/**`, `frontend/src/**/*.test.tsx`만
    - 구현 코드는 만들지 않음
  - `.github/agents/implementer.agent.md`
    - 역할: 실패 테스트를 통과시키는 최소 구현
    - `tests/` 수정 금지, 테스트가 틀렸다고 판단되면 멈추고 보고
  - `.github/instructions/python-tests.instructions.md` (`applyTo: "backend/tests/**"`): 픽스처·네이밍 규칙
- **정답 브랜치 주의:** `members/api.py`에는 `register`, `list_members`만 두고 `get_member`는 넣지 않습니다. 대신 `members/repository.py`에 `get_by_id`를 둡니다. (S2 함정용)
- **verify:**
  - `uv run pytest` 통과, `npm test` 통과
  - 스킬·에이전트 파일 존재
  - `git log`에서 `backend/tests/posts`를 바꾼 첫 커밋이 `backend/app/posts`를 바꾼 첫 커밋보다 앞섬

### S2 팔로우 (30분)

- **목표:** 문장 규칙이 아니라 결정적 장치로 모듈 경계와 위험 행동을 막는다.
- **진행 (분)**
  - 5 — 하네스 없이 팔로우 기능 요청 → `follows`가 `members.repository`를 import하는지 확인
  - 5 — `backend/pyproject.toml`에 import-linter 계약 추가, `uv run lint-imports`로 위반 확인
  - 10 — `.github/hooks/guardrails.json`과 훅 스크립트 2개 작성
  - 3 — `cp templates/workflows/ci.yml .github/workflows/`
  - 7 — Copilot CLI로 같은 요청 재실행 → 위반 시도가 훅에서 차단되고 `members/api.py`에 `get_member`를 추가하는 방향으로 수정되는지 확인
- **import-linter 계약 (예시)**

  ```toml
  [tool.importlinter]
  root_package = "app"

  [[tool.importlinter.contracts]]
  name = "도메인 패키지는 서로의 api만 import"
  type = "forbidden"
  source_modules = ["app.follows", "app.posts", "app.feed", "app.reports"]
  forbidden_modules = ["app.members.repository", "app.members.models", "app.posts.repository", "app.posts.models"]
  # TODO(build): 패키지 전체 조합을 생성 스크립트로 만들거나 layers/independence 계약으로 단순화
  ```

- **훅 설정 (TODO(verify): 공식 hooks reference로 필드명·입출력 확정)**

  ```json
  {
    "version": 1,
    "hooks": {
      "preToolUse": [
        { "type": "command", "bash": "./scripts/hooks/pre_tool_guard.sh", "timeoutSec": 10 }
      ],
      "postToolUse": [
        { "type": "command", "bash": "./scripts/hooks/post_edit_check.sh", "timeoutSec": 120 }
      ]
    }
  }
  ```

  - `pre_tool_guard.sh`
    - stdin JSON에서 도구 이름과 인자를 읽습니다.
    - 다음을 거부합니다:
      - `rm -rf`, `git push --force`, `git reset --hard`
      - `backend/app`·`backend/tests`·`frontend/src` 밖 경로 편집 (`.github/`·`specs/`는 허용)
      - `.env`, `*.db` 파일 편집
    - 거부할 때는 사유를 출력합니다.
  - `post_edit_check.sh`
    - 편집된 파일의 패키지를 찾아 그 패키지의 `pytest backend/tests/<pkg>`와 `lint-imports`를 실행합니다.
    - 실패하면 결과를 에이전트에 돌려줍니다.
- **templates/workflows/ci.yml:**
  - PR · push에서 `uv run pytest`, `uv run lint-imports`, `npm ci && npm test`를 실행합니다.
  - backend/frontend 디렉터리가 비어 있으면 해당 job을 건너뜁니다.
- **VS Code 주의:** VS Code의 훅 지원은 프리뷰이므로 S2는 Copilot CLI로 진행합니다. 가이드 첫 줄에 명시합니다.
- **verify:**
  - `lint-imports` 통과
  - `guardrails.json`이 유효한 JSON이고 preToolUse·postToolUse를 포함
  - 샘플 입력(`scripts/hooks/fixtures/forbidden-edit.json`)을 pre 훅에 넣으면 거부 응답
  - `.github/workflows/ci.yml` 존재

### S3 피드 (15분)

- **목표:** 에이전트가 스키마를 추측하지 않고, 필요한 만큼만 DB를 볼 수 있게 한다.
- **진행 (분)**
  - 3 — `uv run python scripts/seed-db.py`, 하네스 없이 피드 요청 → 추측한 컬럼명(`content`, `created_at`) 오류 관찰
  - 4 — MCP 설정 복사
    - VS Code: `templates/mcp/vscode-mcp.json` → `.vscode/mcp.json`
    - CLI: `/mcp add` 또는 `templates/mcp/copilot-cli-mcp-config.json` 참고 (TODO(verify): CLI 설정 파일 위치)
  - 6 — 같은 요청 재실행 → 에이전트가 `describe_table` 결과로 쿼리 작성, 피드 화면 완성
  - 2 — GitHub MCP로 "피드 페이지네이션" 이슈 생성 → 이슈 번호를 커밋에 연결
- **templates/mcp/sqlite-ro-server/** (Python `mcp` SDK, FastMCP)
  - 도구 3개: `list_tables`, `describe_table(name)`, `query(sql)`
  - `query`는 `SELECT`/`WITH`로 시작하는 단일 문장만 허용합니다.
  - 연결은 `sqlite3.connect("file:<path>?mode=ro", uri=True)`로 이중 차단합니다.
  - DB 경로는 환경변수 `TEAMFEED_DB`로 받습니다. 자격 증명·경로를 저장소에 하드코딩하지 않습니다.
  - 단위 테스트 `test_server.py`: INSERT · UPDATE · DROP · 다중 문장이 거부되는지 확인
- **GitHub MCP:**
  - VS Code는 원격 GitHub MCP 서버(`https://api.githubcopilot.com/mcp/`)를 설정합니다.
  - Copilot CLI는 기본 내장 여부를 Phase 0에서 확인합니다.
- **verify:**
  - `.vscode/mcp.json`에 `sqlite-ro`, `github` 서버 정의
  - `sqlite-ro-server` 단위 테스트 통과
  - 피드 테스트 통과 (숨김 글 제외, 최신순, 본인 글 포함)

### S4 신고 (35분)

- **목표:** 테스트가 통과해도 남는 결함을 작성자와 분리된 리뷰와 결정적 스캔으로 잡는다.
- **진행 (분)**
  - 7 — 하네스 없이 신고 기능 요청 → 테스트는 통과. 그러나 일반 회원이 `PATCH /api/reports/{id}` 호출 시 200인지 `curl`로 확인
  - 5 — Copilot CLI plan 모드로 계획 → `/rubber-duck`으로 다른 모델 계열의 비평 받기 → 계획 수정
  - 8 — `security-reviewer` 에이전트 작성, 리뷰 실행 → 인가 누락이 Critical로 보고되는지 확인
  - 5 — 수정: `require_admin` 추가 + 403 테스트 추가 (test-writer → implementer)
  - 5 — `cp templates/workflows/codeql.yml .github/workflows/`, push, PR 생성
  - 5 — PR에서 Copilot code review 요청, CodeQL 결과 확인 (스캔이 늦으면 강사 화면의 `demo/s4-trap` PR 결과로 설명)
- **파일**
  - `.github/agents/security-reviewer.agent.md`
    - 도구: 읽기·검색만 (TODO(verify): 커스텀 에이전트 `tools` 값)
    - 점검 목록:
      - 상태를 바꾸는 모든 라우트에 인가 의존성이 있는가
      - 403 테스트가 있는가
      - 원시 SQL 문자열 결합이 있는가
      - 오류 응답에 내부 정보가 노출되는가
    - 출력 형식: `Critical / High / Medium` 표, 파일:라인, 근거, 수정 제안
    - 인가 누락은 항상 Critical로 분류하고, 스스로 코드를 수정하지 않습니다.
  - `.github/instructions/security.instructions.md` (`applyTo: "backend/app/**"`): 인가 규칙, 쿼리는 SQLAlchemy 바인딩 파라미터만
  - `templates/workflows/codeql.yml`: python, javascript-typescript 언어. PR · push 트리거
- **CodeQL 전제:**
  - 참가자 저장소가 공개 저장소이거나, 조직에 GitHub Code Security(GHAS) 라이선스가 있어야 합니다.
  - 둘 다 아니면 CodeQL은 강사 데모로 대체합니다. `prerequisites-checklist.md`에 명시합니다.
- **verify:**
  - `security-reviewer.agent.md` 존재, 편집 도구 없음
  - 일반 회원 `PATCH /api/reports/{id}` → 403 테스트 존재·통과
  - `q` 검색 구현에 문자열 결합 SQL 없음 (grep)
  - `codeql.yml` 존재

### S5 패키징 + 내 팀 규칙 (30분)

- **목표:** 저장소에 갇힌 하네스를 플러그인으로 묶어 다른 저장소에 설치하고, 자기 팀 규칙 하나를 더한다.
- **진행 (분)**
  - 8 — `templates/plugin/`을 `plugins/teamfeed-harness/`로 복사, 스킬·에이전트·훅·MCP 설정을 플러그인 구조로 옮기기
  - 5 — 다른 저장소(참가자 계정에 빈 `sandbox` 저장소 생성)에서 플러그인 설치 → `/skills` 등으로 로드 확인 (TODO(verify): 로컬 경로 설치 지원 여부, 안 되면 실습 저장소 자체를 marketplace로 등록)
  - 15 — `templates/team-rule-template.md`로 내 팀 규칙 1개를 스킬 또는 훅으로 작성해 플러그인에 추가, 버전 0.2.0으로 올리기
  - 2 — 강사: 사내 marketplace와 조직 정책으로 검증된 플러그인만 배포하는 흐름 설명 (데모 화면)
- **플러그인 구조 (TODO(verify): Agent Plugins 스키마)**

  ```text
  plugins/teamfeed-harness/
  ├── plugin.json          # $schema, name, version, description
  ├── skills/tdd/SKILL.md
  ├── skills/<my-team-rule>/SKILL.md
  ├── mcp.json             # sqlite-ro (경로는 환경변수)
  └── com.github.copilot/
      ├── agents/          # test-writer, implementer, security-reviewer
      └── hooks/           # guardrails.json + 스크립트
  ```

- **team-rule-template.md:** 규칙 이름 / 우리 팀에서 실제로 새는 상황 / 안내(스킬)로 충분한가 강제(훅)가 필요한가 / 수용 기준 / 예시 입력과 기대 동작
- **verify:**
  - `plugin.json`이 유효한 JSON이고 필수 필드 포함
  - 플러그인 안에 스킬 2개 이상(tdd + 내 팀 규칙), 에이전트 3개, 훅 설정 1개
  - version이 0.1.0이 아님

### 회고 · 자가진단 (15분)

- **10분 — 회고표 채우기** (`labs/99-retro.md`)
  - 열: 함정 6개 × 막은 하네스 × 통제 방식(안내 / 역할 분리 / 강제 / 도구 범위 / 독립 리뷰 / 배포)
  - 강사가 정답표와 비교합니다.
- **5분 — 자가진단 카드** (`templates/self-check-card.md`)
  - 5개 축: 요구·명세 / 설계·경계 / 테스트·검증 / 보안·리뷰 / 배포·운영 (TODO(align): Inno Hub 진단 5개 축 이름과 일치시키기)
  - 각 축에 대해 "우리 팀에서 가장 자주 새는 곳"과 "그 자리에 둘 강제 1개"를 적습니다.

---

## 7. 지원 파일 상세

### 7.1 devcontainer

- 이미지: `mcr.microsoft.com/devcontainers/python:3.12`
- features: Node 22, GitHub CLI
- `post-create.sh`가 설치하는 것:
  - uv
  - Copilot CLI (`npm install -g @github/copilot`, TODO(verify): 패키지명)
  - spec-kit (`uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`)
  - 의존성: `cd backend && uv sync`, `cd frontend && npm ci`
- 확장 프로그램: GitHub Copilot, GitHub Copilot Chat, Python, Pylance, ESLint
- 포트: 8000, 5173 자동 포워딩
- Codespaces prebuild를 설정해 기동 시간을 줄입니다. 목표는 10분 이내입니다.

### 7.2 scripts/verify-step.sh

- 사용법: `scripts/verify-step.sh S0` … `S5`, `ALL` (S0~S5 누적 검사, `final` 브랜치용)
- 각 단계 6장의 verify 항목을 검사하고 `✅ / ❌ 항목명 + 해결 힌트`를 출력합니다.
- 마지막에 통과 개수를 출력하고, 실패 시 종료 코드 1을 반환합니다.
- bash + `jq` + `python -c`만 사용합니다.

### 7.3 requirements/*.md 형식

```text
# 0n <기능명>
## 배경 (2~3문장, 사용자 관점)
## 기능 요건 (번호 목록)
## 수용 기준
- Given <전제> / When <행동> / Then <결과>   (기능당 2~4개, 오류 경로 포함)
## 범위 밖
```

### 7.4 bp-catalog/README.md

| 업계 공통 패턴 | 우리 BP로 바꾼 규칙 | GHCP 구현 | 단계 | 패턴 출처 (각주) |
|---|---|---|---|---|
| 에이전트 행동 원칙 | 가정 말하기, 범위만 수정 | AGENTS.md | S0 | 커뮤니티 원칙 모음 |
| 스펙 주도 개발 | constitution + spec/plan/tasks | spec-kit | S0 | github/spec-kit |
| TDD 강제 | 테스트 커밋 먼저, 테스트 수정 금지 | 스킬 + 역할 분리 에이전트 | S1 | 여러 TDD 스킬 하네스 |
| 위험 명령 차단 | 파괴적 명령·범위 밖 편집 거부 | preToolUse 훅 | S2 | 역할 기반 가상 팀 하네스 |
| 결정적 경계 검사 | api.py 경유 import | import-linter + postToolUse + CI | S2 | 훅 기반 최적화 하네스 |
| 최소 권한 도구 | DB는 읽기 전용 MCP로만 | 커스텀 MCP 서버 | S3 | MCP 보안 권고 |
| 작성자와 분리된 리뷰 | 인가 누락 = Critical | 읽기 전용 리뷰어 + rubber duck | S4 | 2축 리뷰 패턴 |
| 결정적 보안 스캔 | 원시 SQL 금지 | CodeQL | S4 | GitHub Code Security |
| 팀 자산 배포 | 검증된 것만 배포 | Agent Plugins + 사내 marketplace | S5 | GitHub Docs |

각주에만 오픈소스 프로젝트명을 적고, 본문에는 패턴명만 씁니다.

### 7.5 facilitator/

- **run-of-show.md:**
  - 180분 분 단위 진행표(2장 시간표 기준)
  - 단계별 강사 시연 포인트, 늦은 참가자 기준(단계 시간의 70% 경과 시 checkpoint 안내)
  - 휴식 위치(S2 종료 후 15분)
- **prerequisites-checklist.md:**
  - 참가자: GitHub 계정, Copilot Business 또는 Enterprise 라이선스
  - 조직 정책: Copilot CLI 허용, MCP 서버 허용, 프리뷰 기능 허용, Codespaces 사용·할당량
  - CodeQL 전제(공개 저장소 또는 GHAS)
  - 사전 점검 명령: `copilot --version`, `uv --version`, `node -v`, `specify --help`
  - 워크샵 1주 전 안내 메일 문안
- **troubleshooting.md:**
  - 훅이 동작하지 않음 → VS Code 대신 CLI 사용, 실행 권한(`chmod +x`)
  - MCP 연결 실패 → `TEAMFEED_DB` 경로, 인증
  - `uv sync` 지연 → prebuild 확인
  - 포트 포워딩, spec-kit 명령이 안 보임, Copilot 정책 미허용
- **trap-log.md:**
  - 단계 × 시도 1~3 × 모델 × 재현 여부 × 관찰 메모
  - 재현율 2/3 미만이면 요건 조정 또는 demo 브랜치 결정

---

## 8. 구축 Phase (Copilot 작업 순서)

각 Phase 끝에서 멈추고 사람이 검토합니다. 괄호 안은 예상 작업량입니다.

### Phase 0 — 공식 문서로 사양 확정 (0.5일)

- **작업:**
  - 아래 항목을 GitHub Docs와 각 프로젝트 README로 확인해 `docs/authoring/verified-specs.md`에 "값 · 출처 URL · 확인일"로 기록합니다.
  - 이 문서의 모든 `TODO(verify)`를 해소하거나 대안을 적습니다.
- **확인 항목:**
  - 커스텀 인스트럭션 · `*.instructions.md`의 `applyTo` 형식
  - Agent Skills 위치(`.github/skills`)와 SKILL.md frontmatter
  - 커스텀 에이전트 파일 형식과 `tools` 값
  - 훅: 파일 위치, `version`, 이벤트 이름, 스크립트 stdin 형식, 거부 응답 형식, VS Code 지원 수준
  - MCP: VS Code `.vscode/mcp.json` 형식, Copilot CLI 설정 위치와 `/mcp` 명령, GitHub MCP 기본 내장 여부
  - Agent Plugins 1.0 `plugin.json` 스키마, `copilot plugin install`의 로컬 경로·저장소 지원, marketplace 등록 방법
  - spec-kit: 설치 명령, `--integration copilot`, `--here`, 슬래시 명령 이름, 생성 파일 위치
  - Copilot CLI: 설치 패키지명, plan 모드, `/rubber-duck`, `/fleet`
  - awesome-copilot: TDD · 보안 리뷰 관련 에셋 이름 (S1 · S4 출발점)
  - CodeQL: 공개·비공개 저장소 조건
- **완료 기준:** `TODO(verify)` 0개, 또는 남은 항목마다 대안이 기록됨

### Phase 1 — main 골격 (0.5일)

- **작업:** 3.1 구조 중 앱 구현을 뺀 전부(devcontainer, backend·frontend 골격, requirements 6개, templates, scripts 골격, README)
- **완료 기준:**
  - Codespaces 기동 10분 이내
  - 빈 골격에서 `uv run pytest`(0 tests 정상 종료)와 `npm test` 통과
  - main에 금지 파일 없음 (`scripts/verify-step.sh --check-main`)

### Phase 2 — 정답 앱 단계별 구현 (1.5일)

- **작업:** main에서 `s0-done`을 만들고 단계마다 이전 브랜치에서 분기해 4장 명세를 구현합니다.
- **반드시 지킬 의도적 설계:**
  - S1의 `members/api.py`에 `get_member` 없음
  - S1~S2의 비일반적 컬럼명
  - S4 테스트 픽스처 기본 클라이언트 = ADMIN
- **완료 기준:**
  - 각 브랜치에서 `uv run pytest`와 `npm test` 통과
  - s5-done 기준 2,000 LOC 이하

### Phase 3 — 정답 하네스 (1일)

- **작업:**
  - 6장의 파일을 각 `s<n>-done`에 추가하고, 이후 브랜치에 누적합니다.
  - `templates/`의 sqlite-ro MCP 서버와 테스트, 워크플로 2개, 플러그인 골격을 완성합니다.
- **완료 기준:**
  - 각 브랜치에서 `scripts/verify-step.sh S<n>` 통과
  - 훅 스크립트를 fixtures로 테스트
  - MCP 서버 단위 테스트 통과

### Phase 4 — 자동 검증 (0.5일)

- **작업:**
  - `verify-step.sh` 완성
  - 워크샵 저장소 자체의 검증 워크플로 `authoring` 브랜치의 `.github/workflows/verify-branches.yml`: matrix로 `s0-done`~`s5-done`을 체크아웃해 각 단계 verify 실행, `final`은 `ALL`로 실행
- **완료 기준:** matrix 전부 통과

### Phase 5 — 함정 재현 시도 (1일, 사람 + Copilot)

- **작업:**
  - 단계마다 직전 브랜치(S0은 main)에서 하네스를 지운 상태로 가이드의 "하네스 없이 시도" 프롬프트를 3회 실행합니다.
  - 결과를 `facilitator/trap-log.md`에 기록합니다.
  - 정답 하네스를 적용한 상태에서도 3회 실행해 막히는지 기록합니다.
- **판정:**
  - 재현율 2/3 이상이면 그대로 둡니다.
  - 2/3 미만이면 요건 문장이나 재현 장치를 조정하고 다시 시도합니다.
  - 그래도 낮으면 `demo/s<n>-trap` 브랜치를 만들어 강사 시연으로 대체합니다.
- **완료 기준:** 함정 6개 모두 "재현" 또는 "demo 브랜치 준비" 상태

### Phase 6 — 가이드와 강사 문서 (1일)

- **작업:**
  - 6장 형식으로 `labs/` 7개 작성
  - `bp-catalog/README.md`, `facilitator/` 4종, README 완성
  - 프롬프트는 복사해 바로 쓸 수 있게 코드 블록으로 작성
- **완료 기준:** 처음 보는 사람이 가이드만으로 S0~S5를 끝낼 수 있음 (내부 1명 블라인드 테스트)

### Phase 6.5 — `final` 브랜치 (0.5일)

- **작업:** `s5-done`에서 `final`을 분기해 3.3의 내용을 채웁니다. 화면 캡처와 PR 이력은 실제로 실행해서 남깁니다.
- **완료 기준:** `scripts/verify-step.sh ALL` 통과, README만 읽어도 완성 모습과 하네스 구조를 이해할 수 있음

### Phase 7 — 리허설과 마무리 (0.5일)

- **작업:**
  - `final` 브랜치에 태그 `v1.0`을 붙입니다.
  - 2~3명이 실제 시간으로 리허설합니다.
  - 단계별 소요 시간과 막힌 지점을 `docs/authoring/rehearsal.md`에 기록하고 가이드·시간표를 조정합니다.
  - main에서 금지 파일 최종 점검, 템플릿 저장소로 설정합니다.
- **완료 기준:** 1.2의 저장소 전체 완료 기준 전부 체크

총 예상: 약 7일 (Phase 5 · 7은 사람 참여 필요)

---

## 9. 위험과 대응

| 위험 | 대응 |
|---|---|
| Greenfield라 참가자 결과가 제각각 | 단계 시작 전에 checkpoint로 맞출 수 있게 안내, 단계 시간 70% 경과 시 합류 권장 |
| 모델이 똑똑해져 함정이 재현되지 않음 | Phase 5 재현 기록, demo 브랜치로 강사 시연 대체. 메시지를 "가끔 새는 것을 항상 막는다"로 유지 |
| 훅·플러그인 사양 변경 | Phase 0 verified-specs를 워크샵 1주 전 재확인, 변경 시 가이드만 수정 |
| 조직 정책으로 CLI · MCP · 프리뷰 기능 차단 | 사전 점검 체크리스트, 차단 시 해당 단계는 강사 시연 + 파일 작성만 진행 |
| CodeQL 사용 불가 (비공개 저장소, GHAS 없음) | 강사 데모 PR로 대체, 리뷰어 에이전트 실습은 그대로 진행 |
| 시간 초과 | S3는 템플릿 복사만으로 끝낼 수 있게 설계, S5 팀 규칙 작성은 10분으로 줄일 수 있게 템플릿 제공 |

---

## 10. 덱과 맞출 용어

덱 v2(AI-DLC-Developer-Workshop.pptx) 세션 3의 단계명, 시간, 하네스 이름, 회고표와 이 저장소의 가이드가 같은 단어를 쓰는지 Phase 6에서 대조합니다. 대상 용어:

- constitution · 인스트럭션
- TDD 스킬 · 역할 분리
- 경계 훅 · CI 게이트
- GitHub · DB MCP
- 보안 리뷰어 · CodeQL
- 팀 플러그인
- 함정 6개 이름
