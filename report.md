# Spec Kit 기반 TeamFeed Hands On Lab 실검증 및 워크샵 개선 보고서

- **문서 목적**: Agenda 3 Hands On Lab(180분 실습)의 실제 환경 구성, 1차 기술 검증 결과 분석, 워크샵 핵심 스크립트/보안 가드레일 전면 개선, 그리고 2차 재검증 결과 정리
- **대상 워크샵**: GitHub Spec Kit 기반 SDD(Specification-Driven Development) & GitHub Copilot 개발자 워크샵
- **최종 검증 일시**: 2026-10-12
- **저장소 브랜치**: daeungo1/msft-ghcp-dev-workshop (s1-done)

---

## 1. 결과 요약 (Executive Summary)

GitHub Spec Kit 공식 CLI와 Copilot Extensions를 활용하여 TeamFeed 워크샵 전 단계(S0~S5)에 대한 실제 환경 검증을 수행하였다. 
1차 실검증 과정에서 Windows 환경의 CLI 호환성 결함, 가드레일의 Fail-Open 보안 취약점, 터미널 인코딩 충돌 등 실제 교육 현장에서 실습생들을 가로막을 수 있는 4가지 핵심 결함을 식별하였다.

본 2차 작업에서는 식별된 결함을 근본적으로 해결하기 위해 워크샵 검증 스크립트(`scripts/verify-step.sh`) 및 S2 가드레일 템플릿(`templates/starter/s2/*`) 전반을 전면 개편하고, 재검증 테스트를 거쳐 안전하고 신뢰할 수 있는 워크샵 환경을 완성하였다.

### 종합 검증 현황 요약

| 검증 영역 | 1차 검증 관측치 | 2차 개선 및 재검증 결과 | 개선 상태 |
|---|---|---|---|
| **S1 단계 검증 스크립트** | Windows Store python3 alias로 인해 exit code 49 비정상 종료 | Python 유효성 실검증 및 스마트 폴백 적용으로 `6/6 전수 통과` | **해결 완료 (Green)** |
| **S2 보안 가드레일** | 인코딩/런타임 예외 발생 시 `allow` 방출 (CWE-276 Fail-Open 취약점) | 예외 발생 시 `deny` 차단하는 `Fail-Closed` 보안 아키텍처로 전면 수정 | **해결 완료 (Secure)** |
| **Windows 콘솔 인코딩** | 한글 에러 사유 출력 시 CP949 charmap 인코딩 예외 발생 | `sys.stdin`/`sys.stdout` UTF-8 reconfigure 강제 적용 완료 | **해결 완료 (Clean)** |
| **패키지 동기화 네트워크** | 폐쇄망/오프라인 환경에서 `uv run` 호출 시 index sync 핸드셰이크 실패 | `--no-sync` 옵션을 기본 매개변수로 명시하여 안정적 오프라인 구동 보장 | **해결 완료 (Offline-ready)** |
| **백엔드 단위 테스트** | S1 요구사항에 대한 pytest 단위 테스트 통과 | `uv run --no-sync pytest` 실행 결과 `9/9 전수 통과` 확인 | **검증 완료 (Green)** |
| **S2 Hook Fixture 테스트** | bash 및 python 경로 미감지로 인한 실행 실패 | 파이프라인 및 인자 처리 정상 통과 확인 | **검증 완료 (Green)** |

---

## 2. 워크샵 환경 및 아키텍처 개요

### 2.1 핸즈온 랩 (S0 ~ S5)과 Spec Kit 워크플로우 매핑

워크샵은 총 180분(실습 165분 + 회고 15분)으로 구성되며, Spec Kit의 6대 핵심 프롬프트와 1:1로 결합되어 체계적인 SDD 개발 흐름을 교육하도록 설계되었다.

```
[S0. 프로젝트 헌법/도메인 규칙]  <--->  /speckit-constitution  (Constitution 정립)
                 │
[S1. 회원/글 도메인 및 TDD]    <--->  /speckit-specify & /speckit-plan & /speckit-tasks
                 │
[S2. 경계 보호 및 에이전트 훅]  <--->  /speckit-implement     (Fail-Closed 가드레일)
                 │
[S3. 피드 집계 및 MCP 연동]    <--->  /speckit-implement     (SQLite / GitHub MCP)
                 │
[S4. 관리자 기능 및 독립 리뷰]  <--->  /speckit-converge      (Security Review & 수렴)
                 │
[S5. 패키징 및 확장 공유]      <--->  GitHub Copilot Extension / Plugin 패키징
```

---

## 3. 주요 결함 분석 및 워크샵 코드 개선 내역 (Deep Dive)

1차 실검증에서 발굴되어 이번 업데이트를 통해 근본적으로 개선된 4대 결함과 패치 상세 내역은 다음과 같다.

### 결함 1: Windows Store App Execution Alias (`python3`) 크래시 (Exit code 49)
- **원인 분석**:
  Windows 10/11에서는 환경 변수 PATH에 `WindowsApps/python3.exe` 가상 실행 파일이 기본 등록되어 있어, Git Bash나 일반 터미널에서 `command -v python3` 검사를 수행하면 0(성공)을 반환한다. 그러나 실제 실행 시 Microsoft Store 팝업이 뜨거나 프로세스가 **exit code 49**로 강제 종료되어 워크샵 스크립트 전체가 중단되는 현상이 발생했다.
- **적용된 개선 패치**:
  단순 파일 존재 여부가 아닌, 인터프리터에 `-c "import sys"` 명령을 직접 전달하여 실제 유효성을 실검사하는 감지 루틴을 구현하였다.
  ```bash
  # scripts/verify-step.sh 및 templates/starter/s2/test_hooks.sh
  PYTHON_CMD=""
  for cmd in python3 python py; do
    if command -v "$cmd" >/dev/null 2>&1 && "$cmd" -c "import sys" >/dev/null 2>&1; then
      PYTHON_CMD="$cmd"
      break
    fi
  done
  ```

### 결함 2: S2 보안 가드레일 Fail-Open 취약점 (CWE-276)
- **원인 분석**:
  기존 `templates/starter/s2/pre_tool_guard.skeleton.sh`의 JSON 파싱 및 규칙 검증 로직은 예외가 발생할 경우 `except Exception: emit("allow")` 처리를 하도록 작성되어 있었다. 이로 인해 잘못된 JSON 입력, 파싱 예외, 콘솔 인코딩 에러 등이 발생하면 **위험한 명령어(예: `rm -rf`, 승인되지 않은 SQL 쓰기 등)가 그대로 승인(Allow)**되는 심각한 보안 취약점(CWE-276: Default Allow)이 내포되어 있었다.
- **적용된 개선 패치**:
  보안 제어의 기본 원칙인 **Fail-Closed (기본 차단)** 원칙을 엄격하게 적용하였다.
  ```python
  # templates/starter/s2/pre_tool_guard.skeleton.sh
  except Exception as e:
      # Fail-closed: 예외 발생 시 보안을 위해 반드시 차단
      emit("deny", f"보안 가드레일 오류로 인해 명령이 차단되었습니다: {str(e)}")
  ```

### 결함 3: Windows 콘솔 CP949 인코딩 충돌 (`charmap` error)
- **원인 분석**:
  Windows Git Bash 및 명령 프롬프트 환경에서 Python의 기본 인코딩은 시스템 로캘(CP949)을 따른다. 가드레일 훅이 한글 차단 사유(예: `"rm -rf 명령어는 금지되어 있습니다"`)를 표준 출력으로 방출할 때 `UnicodeEncodeError: 'charmap' codec can't encode characters`가 발생하여 훅이 비정상 종료되었다.
- **적용된 개선 패치**:
  인라인 Python 스크립트 실행 최상단에 표준 입출력 스트림을 UTF-8로 강제 재구성(`reconfigure`)하는 방어 코드를 모든 스크립트에 일괄 적용하였다.
  ```python
  import sys
  if hasattr(sys.stdin, "reconfigure"):
      sys.stdin.reconfigure(encoding="utf-8")
  if hasattr(sys.stdout, "reconfigure"):
      sys.stdout.reconfigure(encoding="utf-8")
  ```

### 결함 4: 오프라인/사내망 환경 `uv run` 인덱스 동기화 에러 방지
- **원인 분석**:
  기업 교육장이나 사내 보안망, 오프라인 환경에서 `uv run`을 호출하면 원격 PyPI 인덱스와 패키지 락 동기화를 시도하다가 `HandshakeFailure` 또는 타임아웃 에러가 발생하여 실습이 중단되는 문제가 있었다.
- **적용된 개선 패치**:
  `scripts/verify-step.sh` 및 `templates/starter/s2/post_edit_check.sh`에 `uv run --no-sync` 플래그를 기본값으로 지정하여 외부 네트워크 요청 없이 로컬 가상환경에서 즉시 고속 실행되도록 최적화하였다.

---

## 4. 2차 검증 및 테스트 결과 (Verification Evidence)

스크립트 수정 후 실제 터미널 환경에서 재검증을 수행하였으며, 모든 테스트가 결함 없이 완벽히 통과함을 확인하였다.

### 4.1 `verify-step.sh S1` 자동 검증 결과
```
[PASS] S1-1: spec.md 존재
[PASS] S1-2: plan.md 존재
[PASS] S1-3: tasks.md 존재
[PASS] S1-4: backend/app/members/routes.py 존재
[PASS] S1-5: backend/app/posts/routes.py 존재
[PASS] S1-6: backend/tests/members/ 또는 posts/ 테스트 통과
=== S1 검증 결과: 통과 (passed: 6, failed: 0) ===
```

### 4.2 백엔드 단위 테스트 결과 (`uv run --no-sync pytest`)
```
============================= test session starts =============================
platform win32 -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: C:\Users\daeungo\ghcp-dev-workshop\backend
configfile: pyproject.toml
collected 9 items

tests/members/test_members.py ....                                       [ 44%]
tests/posts/test_posts.py .....                                          [100%]

============================== 9 passed in 0.52s ==============================
```

### 4.3 S2 가드레일 Hook Fixture 테스트 결과
`templates/starter/s2/test_hooks.sh` 실행 시, 인코딩 크래시나 파이썬 버전 오류 없이 JSON 페이로드를 정상 파싱하고 스켈레톤 인자를 유효하게 처리함을 검증하였다.

---

## 5. 워크샵 진행자를 위한 종합 가이드 (Facilitator Guide)

### 5.1 강사/진행자 사전 준비 체크리스트
1. **Python 인터프리터 경로 점검**:
   - 수강생들의 PC에 설치된 Python이 Microsoft Store Alias와 충돌하지 않는지 확인한다.
   - 필요 시 Windows "앱 실행 별칭(Manage App Execution Aliases)" 설정에서 `python.exe` 및 `python3.exe`를 비활성화하도록 사전 안내한다.
2. **사전 가상환경 빌드**:
   - `cd backend && uv venv && uv sync`를 미리 완료하여 오프라인 환경에서도 `--no-sync`로 즉시 테스트가 가능하도록 준비한다.
3. **콘솔 인코딩 환경 변수 설정**:
   - `export PYTHONUTF8=1` 또는 `$env:PYTHONUTF8="1"`을 기본 터미널 프로필에 추가하도록 권장한다.

### 5.2 단계별(S0~S5) 핵심 코칭 포인트
- **S0 (Constitution)**: 규칙을 너무 많이 넣지 않고, `app.errors` 사용과 도메인 레이어 분리(`routes`, `service`, `repository`) 원칙을 명확히 설정하도록 유도한다.
- **S1 (TDD & Spec)**: 실패하는 테스트(RED)가 커밋되기 전에 구현(GREEN)을 작성하지 않도록 TDD 워크플로우를 점검한다.
- **S2 (Fail-Closed 가드레일)**: 예외 발생 시 보안 가드레일이 반드시 차단(Deny)해야 하는 이유를 CWE-276 사례와 연결하여 설명한다.
- **S3 (MCP)**: SQLite MCP를 통한 실시간 스키마 탐색 및 안전한 읽기 전용 질의 작성법을 교육한다.
- **S4 (Security Review)**: `security-reviewer` 커스텀 서브에이전트를 활용하여 권한 검사 누락 및 SQL 바인딩 파라미터 준수 여부를 검증한다.
- **S5 (Extension)**: 완성된 산출물과 스킬을 재사용 가능한 팀 플러그인 규격으로 패키징하는 실습을 진행한다.

---

## 6. 결론

본 개편을 통해 Spec Kit 기반 Hands On Lab 워크샵은 **크로스 플랫폼 호환성**, **Fail-Closed 보안 가드레일**, **오프라인 안정성**을 모두 확보하였다. 강사와 수강생 모두 환경 설정 이슈나 플랫폼 종속적인 오류에 방해받지 않고, GitHub Copilot과 Spec Kit이 제공하는 Specification-Driven Development(SDD)의 본질적인 개발 생산성 혁신을 온전히 체감할 수 있을 것이다.
