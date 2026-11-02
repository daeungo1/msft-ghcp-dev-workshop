---
description: TeamFeed React 프론트엔드의 타입 안전성과 API 오류 처리 규칙
applyTo: "frontend/src/**/*.{ts,tsx}"
---

# 프론트엔드 규칙

* TypeScript `any`를 사용하지 않습니다.
* API 호출은 `src/api.ts`의 공통 요청 함수를 통과합니다.
* 백엔드 오류의 `error.message`를 사용자에게 표시하고 실패를 성공처럼
  처리하지 않습니다.
* 서버 권한 검사를 UI 가시성으로 대체하지 않습니다.
* 수용 기준마다 사용자 관점의 컴포넌트 테스트를 하나씩 작성합니다.

