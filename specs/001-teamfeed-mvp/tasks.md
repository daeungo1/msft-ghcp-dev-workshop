# 작업 목록: TeamFeed MVP

각 기능은 "테스트 먼저, 구현 다음" 순서입니다. 한 줄이 커밋 하나에 해당합니다.

## S1 회원과 게시글 (US1)

- [ ] T101 members, posts 수용 기준을 실패하는 테스트로 작성 (`backend/tests/members`, `backend/tests/posts`)
- [ ] T102 members, posts 백엔드 구현
- [ ] T103 회원 선택, 글쓰기 폼, 글 목록 화면

## S2 팔로우 (US2)

- [ ] T201 follows 수용 기준을 실패하는 테스트로 작성
- [ ] T202 follows 백엔드 구현 (다른 패키지는 `api.py`로만 호출)
- [ ] T203 글 옆에 팔로우, 해제 버튼

## S3 피드 (US3)

- [ ] T301 feed 페이지 나누기 테스트 작성
- [ ] T302 feed 구현 (실제 DB 스키마를 확인한 뒤 작성)
- [ ] T303 피드 화면

## S4 신고 (US4)

- [ ] T401 reports 수용 기준과 403 테스트 작성
- [ ] T402 reports 구현 (관리자 검사, 바인딩 파라미터)
- [ ] T403 신고 버튼과 관리자 화면
