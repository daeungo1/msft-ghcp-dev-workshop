---
title: 워크샵 이후 다음 단계
description: 이 워크샵의 하네스를 고객 저장소 맞춤 AI-native SDLC로 확장하는 경로와 레퍼런스 구현
---

워크샵에서 만든 하네스는 우리 팀 BP의 첫 번째 버전입니다. 다음 버전은 실제 저장소에서 만듭니다.
발표 자료 4번 Agenda(슬라이드 26~29)를 이 저장소 기준으로 이어 쓴 안내입니다.

## 권장 순서

| 단계 | 하는 일 | 이 워크샵에서 가져갈 것 |
|---|---|---|
| 1 SDLC 진단 | 우리 팀 병목과 새는 지점을 진단 | [templates/self-check-card.md](../templates/self-check-card.md) 결과 |
| 2 하네스 설계 | 새는 지점마다 안내로 둘지 강제로 올릴지 결정 | [templates/team-rule-template.md](../templates/team-rule-template.md), [bp-catalog](../bp-catalog/README.md) |
| 3 PoC (2주 안팎) | 실제 저장소 하나에 하네스를 적용하고 지표 측정 | `plugins/teamfeed-harness/`를 설치하고 규칙 1개씩 교체 |
| 4 확산 | 검증된 하네스를 사내 marketplace로 배포 | `.github/plugin/marketplace.json` 형식 (final 브랜치 참고) |

## PoC 범위 정하기

* 병목 한 곳만 고릅니다. 자가진단 카드에서 가장 비싼 칸입니다.
* 강제 하나를 먼저 둡니다. 훅이나 CI 게이트처럼 사람이 없어도 동작하는 것부터 시작합니다.
* 측정 지표를 먼저 정합니다. 예: 리뷰 왕복 횟수, CI 실패율, 경계 위반 건수.
* 에이전트가 우회할 수 있는 안내는 지표가 좋아졌는지 확인한 뒤에 늘립니다.

## 레퍼런스 구현

[HakjunMIN/ai-native-harness](https://github.com/HakjunMIN/ai-native-harness)는 사람 승인을 세 지점에만 두고 나머지는 증거로 통과시키는 레퍼런스입니다.
이 워크샵의 구현과 달라도 원칙은 같습니다.

| 원칙 | 이 워크샵에서 | 레퍼런스에서 |
|---|---|---|
| 사람은 판단, 기계는 검증 | 훅과 CI가 규칙을 강제 | 승인 지점 외에는 증거 기반 통과 |
| 증거가 있어야 완료 | `verify-step.sh`, 테스트 | 자동 검증 결과 첨부 |
| 작성자와 검토자 분리 | `security-reviewer`, rubber duck | 독립 검증 단계 |

## 팀에서 이어 할 일 체크리스트

* [ ] 자가진단 카드를 팀원과 함께 다시 채우고 의견 차이를 기록
* [ ] 새는 지점 상위 3개를 안내, 강제 중 어느 쪽으로 풀지 정리
* [ ] PoC 대상 저장소와 담당자 확정
* [ ] 플러그인을 PoC 저장소에 설치해 보고 규칙 1개를 팀 규칙으로 교체
* [ ] 2주 뒤 지표로 회고

더 구체적인 진행은 Microsoft Innovation Hub와 함께 설계합니다.
