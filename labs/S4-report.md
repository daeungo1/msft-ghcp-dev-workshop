---
title: S4 신고 (35분)
description: 테스트가 통과해도 새는 인가 누락을 작성자와 분리된 읽기 전용 리뷰어와 CodeQL로 잡습니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 35분 (시도 6, 관찰 4, 하네스 추가 9, 재실행·리뷰 13, 확인 3) |
| 도구 | Copilot CLI (rubber duck, 리뷰어 에이전트), GitHub (CodeQL, Copilot code review) |
| 시작 상태 | S3 완료 (`s3-done`) |
| 완료 상태 | `s4-done` 브랜치와 같은 수준 |
| 통제 방식 | 독립 리뷰 |
| 막는 함정 | 관리자 인가 누락. 기능 테스트는 통과함 |

## 이 단계에서 배우는 것

* 코드를 쓴 에이전트는 자기 코드의 인가 누락을 잘 보지 못합니다. 작성자와 분리된 리뷰어가 필요합니다.
* 리뷰어는 읽기 전용이어야 합니다. 고칠 수 있는 리뷰어는 리뷰하다 코드를 바꿉니다.
* 서로 다른 모델의 눈(rubber duck), 결정적 스캐너(CodeQL), 사람 리뷰 보조(Copilot code review)를 겹칩니다.

## 시작 전 확인

```bash
git status --short
scripts/checkpoint.sh S3      # S3를 건너뛰었다면 정답 상태에서 시작
```

## 추가 요건

[requirements/04-report.md](../requirements/04-report.md): 신고, 관리자 처리, 숨김.

## 1. 하네스 없이 시도 (6분)

```text
requirements/04-report.md 를 백엔드와 프론트엔드 모두 구현해줘. 테스트도 함께 작성해줘.
```

## 2. 관찰 (4분)

테스트는 통과합니다. 이제 기능 테스트가 보지 못하는 것을 직접 확인합니다.

```bash
cd backend && uv run pytest -q && cd ..
```

앱을 실행하고(`scripts/dev.sh`) 일반 회원(관리자가 아닌 `X-Member-Id`)으로 관리자 기능을 호출해 봅니다. 회원 ID는 앱에서 가입한 값을 사용합니다.

```bash
# 일반 회원(ID 2)이 신고 목록을 조회
curl -s -H "X-Member-Id: 2" "http://localhost:8000/api/reports?status=OPEN"
# 일반 회원이 신고를 승인
curl -s -X PATCH -H "X-Member-Id: 2" -H "Content-Type: application/json" \
  -d '{"status":"ACCEPTED"}' http://localhost:8000/api/reports/1
```

* 403이 아니라 200이 나오면 인가 누락입니다. 화면에서만 관리자 탭을 숨기고 API는 열려 있는 흔한 패턴입니다.
* 검색어 `q` 처리도 읽어 봅니다. 문자열을 이어 붙여 SQL을 만들었는지 보세요.

이 구현을 지우지 않고 그대로 리뷰 대상으로 둡니다.

## 3. 하네스 추가 (9분)

### 3-1. 읽기 전용 리뷰어 에이전트 (5분)

[templates/starter/s4/](../templates/starter/s4/)의 스타터를 복사해 TODO를 채웁니다.

```bash
cp templates/starter/s4/security-reviewer.agent.starter.md .github/agents/security-reviewer.agent.md
```

* `tools`에는 읽기 도구(`read`, `search`)만 둡니다. `edit`, `create`, `write`, `execute`를 넣지 않습니다. `scripts/verify-step.sh S4`가 이를 검사합니다.
* 심각도 기준에 "권한 없는 사용자가 관리자 기능을 쓸 수 있음 = Critical"을 명시합니다.
* 보고 형식은 파일과 줄, 심각도, 재현 방법, 수정 제안입니다.

### 3-2. CodeQL 워크플로 (2분)

```bash
cp templates/workflows/codeql.yml .github/workflows/codeql.yml
```

CodeQL은 공개 저장소이거나 GitHub Code Security가 있어야 결과가 나옵니다. 불가능하면 강사 화면의 데모 PR 결과로 대체합니다.

### 3-3. 변경 사항 커밋과 푸시 준비 (2분)

```bash
git add -A && git commit -m "feat: add reports and security reviewer"
```

## 4. 같은 요청 재실행과 리뷰 (13분)

### 4-1. 리뷰어 에이전트 실행 (4분)

Copilot CLI에서 `/agent`로 `security-reviewer`를 선택하고 실행합니다.

```text
backend/app/reports 의 변경을 리뷰해줘. 인가, 입력 검증, SQL 관점으로 보고하고 Critical부터 정렬해줘.
```

* 리뷰어가 "일반 회원이 PATCH /api/reports 를 호출할 수 있다"를 Critical로 보고하는지 확인합니다.
* 리뷰어는 파일을 고치지 않고 보고만 합니다.

### 4-2. rubber duck으로 두 번째 의견 (3분)

Copilot CLI에는 다른 모델의 눈으로 비평하는 `rubber duck` 에이전트가 내장되어 있습니다.

```text
/rubber-duck 방금 리뷰한 reports 구현에서 놓친 위험이 있는지 비평해줘.
```

### 4-3. 수정과 테스트로 고정 (4분)

기본 에이전트(또는 `implementer`)에게 수정을 맡깁니다. 이때 테스트를 먼저 씁니다.

```text
리뷰 결과를 반영해줘. 먼저 "일반 회원의 GET, PATCH /api/reports 는 403" 테스트를 추가하고, 실패하는 것을 확인한 뒤 구현을 고쳐줘. 검색어 q 는 바인딩 파라미터로 처리해줘.
```

### 4-4. PR로 올려 CodeQL과 Copilot code review 확인 (2분, 선택)

```bash
git switch -c s4-reports && git push -u origin s4-reports
gh pr create --fill
```

PR 화면에서 **Reviewers**에 **Copilot**을 추가해 리뷰를 요청하고, **Checks**에서 CodeQL 실행 여부를 확인합니다.

## 5. 완료 확인 (3분)

```bash
scripts/verify-step.sh S4
```

| 확인 항목 | 안 되면 |
|---|---|
| `security-reviewer`가 읽기 전용 | `tools`에서 쓰기 계열 제거 |
| `backend/tests/reports`에 403 테스트 존재 | 4-3 참고 |
| 백엔드 테스트 통과 | 실패 메시지를 에이전트에게 전달 |
| `backend/app/reports`에 문자열로 만든 SQL 없음 | 바인딩 파라미터 사용 |
| `.github/workflows/codeql.yml` 존재 | 3-2 참고 |

## 정리

* 작성자와 리뷰어를 분리하고, 리뷰어에게는 쓰기 권한을 주지 않습니다.
* 인가 누락처럼 기능 테스트가 보지 못하는 결함은 "인가 테스트"로 고정해 다시 새지 않게 합니다.

## 막히면

* 서로 다른 의견이 나오면 정답 브랜치의 리뷰어 지침과 비교해 보세요.
* 시간이 부족하면 4-4를 건너뛰고 `scripts/checkpoint.sh S4`로 정답 상태에서 합류합니다.

## 정답 보기

```bash
git diff s3-done..s4-done --stat
git show s4-done:.github/agents/security-reviewer.agent.md
git show s4-done:backend/tests/reports
```

## 업계 공통 패턴

작성자와 분리된 리뷰, 결정적 보안 스캔. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
