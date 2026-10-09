---
title: GitHub Copilot 개발자 워크샵 Hands-on Lab
description: 빈 저장소에서 TeamFeed를 만들며 우리 팀 BP를 GitHub Copilot 하네스로 한 겹씩 쌓는 180분 핸즈온 실습 저장소
---

> [!NOTE]
> 초안(v0.1) 상태입니다. 핵심 골격만 담았으며 단계 가이드, 정답 브랜치, 검증 스크립트는 이후 구체화합니다.

## 워크샵 소개

AI-DLC 개발자 워크샵 세션 3 「트렌드 Harness 워크샵 (GHCP 기반)」의 실습 저장소입니다.
참가자는 빈 저장소에서 사내 미니 SNS **TeamFeed**를 GitHub Copilot으로 직접 만들면서,
기능 하나마다 그 기능에서 터지는 문제를 막는 하네스를 한 겹씩 붙입니다.

하네스는 에이전트가 우리 팀의 방식대로 일하도록 감싸는 맥락(Context), 도구(Tools),
흐름 제어(Control Flow), 피드백(Feedback) 장치의 묶음입니다.
인스트럭션과 스킬은 확률적 안내이고, 훅, 테스트, CI, 리뷰 게이트는 결정적 강제입니다.

## 워크샵이 끝나면 남는 것

| 결과물 | 위치 | 내용 |
|---|---|---|
| 동작하는 앱 | `backend/`, `frontend/` | FastAPI 백엔드 + React 피드 화면 (회원, 게시글, 팔로우, 피드, 신고) |
| 팀 하네스 자산 | `.github/`, `AGENTS.md` | constitution, 커스텀 인스트럭션, 스킬, 커스텀 에이전트, 훅, MCP 설정 |
| 팀 플러그인 | `plugins/teamfeed-harness/` | 내 팀 규칙 1개를 더한 BP 패키지, 다음 프로젝트에서 한 줄로 설치 |

## 시간표 (180분)

| 단계 | 시간 | 추가 요건 | 붙이는 하네스 | 막는 함정 | 통제 방식 |
|---|---|---|---|---|---|
| [S0 Spec](labs/S0-spec.md) | 25분 | 앱 비전, MVP | constitution, copilot-instructions.md, AGENTS.md, spec/plan/tasks | 프롬프트마다 구조와 스타일이 달라짐 | 안내 |
| [S1 회원·게시글](labs/S1-member-post.md) | 30분 | 가입, 글 작성·목록, 피드 화면 뼈대 | `tdd` 스킬, `test-writer`·`implementer` 에이전트 | 테스트 없이 완료 보고 | 안내 + 역할 분리 |
| [S2 팔로우](labs/S2-follow.md) | 30분 | 팔로우, 언팔로우 | import-linter, pre·postToolUse 훅, PR CI | 저장소 코드 직접 import | 강제 |
| 휴식 | 15분 | | | | |
| [S3 피드](labs/S3-feed.md) | 15분 | 팔로우한 사람 글 모아 보기 | 읽기 전용 SQLite MCP, GitHub MCP | 스키마를 추측한 쿼리 | 도구 범위 제한 |
| [S4 신고](labs/S4-report.md) | 35분 | 신고, 관리자 처리 화면 | `security-reviewer` 에이전트, rubber duck, CodeQL, Copilot code review | 관리자 인가 누락 | 독립 리뷰 |
| [S5 패키징](labs/S5-package.md) | 30분 | 다음 프로젝트에서 재사용 | 팀 플러그인 + 내 팀 규칙 1개 | 하네스가 저장소에 갇힘 | 배포·재사용 |
| [회고·자가진단](labs/99-retro.md) | 15분 | | 함정 6개 회고표, 자가진단 카드 | | |

## 단계별 진행 방식

모든 단계는 같은 6단계 루프를 따릅니다.

1. `requirements/`에서 기능 요건과 Given/When/Then 수용 기준을 읽습니다.
2. 하네스 없이 Copilot에게 그대로 구현을 요청합니다.
3. 요건 속 함정이 실제로 재현되는지 관찰합니다.
4. 공식 기능으로 우리 BP 하네스를 추가합니다.
5. 같은 프롬프트로 다시 구현을 요청합니다.
6. `scripts/verify-step.sh S<n>`으로 완료를 확인합니다.

> [!TIP]
> 관찰 포인트는 "인스트럭션은 가끔 지켜지고, 훅과 리뷰어는 반드시 막는다"는 차이입니다 (S2, S4).

## 시작하기

1. 이 저장소 상단의 **Use this template**를 눌러 내 계정에 저장소를 만듭니다. **Include all branches**를 반드시 체크합니다.
2. 내 저장소에서 **Code > Codespaces > Create codespace on main**으로 개발 환경을 엽니다.
3. 터미널에서 사전 점검 명령을 실행합니다.

   ```bash
   copilot --version
   uv --version
   node -v
   specify --help
   ```

4. [labs/S0-spec.md](labs/S0-spec.md)부터 순서대로 진행합니다.

> [!IMPORTANT]
> main 브랜치에는 하네스 파일(`.github/copilot-instructions.md`, `AGENTS.md`, `.github/agents`, `.github/skills`, `.github/hooks`)이 의도적으로 없습니다.
> "하네스 없이 시도"에서 함정을 재현하기 위해서입니다.

## 늦었을 때: 체크포인트 브랜치

단계마다 정답 상태가 `s0-done` … `s5-done` 브랜치에 있습니다.
단계 시간의 70%가 지났다면 직전 단계 정답으로 이동해 다음 단계에 합류합니다.

```bash
scripts/checkpoint.sh S2   # s2-done 상태로 work/s2 브랜치 생성
```

## 저장소 구조

```text
msft-ghcp-dev-workshop/
├── .devcontainer/      # Python 3.12, uv, Node 22, GitHub CLI, Copilot CLI, spec-kit
├── backend/            # FastAPI 골격 (의존성만)
├── frontend/           # React + Vite 골격 (의존성만)
├── requirements/       # 단계별 요건 + 수용 기준
├── labs/               # 단계 가이드 S0~S5, 회고
├── bp-catalog/         # 업계 공통 패턴 → 우리 BP → GHCP 기능 매핑
├── templates/          # 사전 제공 자산 (워크플로, MCP, 플러그인 골격, 팀 규칙, 자가진단 카드)
├── scripts/            # verify-step.sh, checkpoint.sh, seed-db.py
└── facilitator/        # 강사용 진행표, 사전 준비, 트러블슈팅, 함정 재현 기록
```

| 브랜치 | 내용 |
|---|---|
| `main` | 참가자 진입점. 앱 골격과 요건, 가이드, 템플릿만 포함 |
| `s0-done` … `s5-done` | 단계 완료 시점의 정답 앱 + 누적 하네스 (구축 예정) |
| `authoring` | 구축 계획(Plan.md)과 작성자 문서 |

## 사전 준비

* GitHub 계정과 Copilot Business 또는 Enterprise 라이선스
* 조직 정책에서 Copilot CLI, MCP 서버, 프리뷰 기능 사용 허용
* GitHub Codespaces 또는 VS Code + Dev Containers
* CodeQL 실습은 공개 저장소이거나 GitHub Code Security 라이선스가 필요합니다

자세한 내용은 [facilitator/prerequisites-checklist.md](facilitator/prerequisites-checklist.md)를 참고합니다.

## 참고 자료

* [GitHub Docs: Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
* [GitHub Docs: Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)
* [GitHub Docs: Plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
* [GitHub Docs: Copilot CLI rubber duck](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck)
* [github/spec-kit](https://github.com/github/spec-kit)
* [github/awesome-copilot](https://github.com/github/awesome-copilot)
* [microsoft/hve-core](https://github.com/microsoft/hve-core)
* [HakjunMIN/ai-native-harness](https://github.com/HakjunMIN/ai-native-harness) (워크샵 이후 고객 저장소 맞춤 하네스 레퍼런스)
