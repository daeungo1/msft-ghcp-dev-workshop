---
title: 04 신고
description: S4 요건. 게시글 신고와 관리자 처리 화면
---

## 배경

구성원은 부적절한 글을 신고합니다.
관리자는 신고 목록을 검색하고 승인 또는 반려합니다. 승인된 글은 숨김 처리됩니다.

## 기능 요건

1. `POST /api/posts/{id}/reports`: 사유(`reason`)와 함께 글을 신고합니다.
2. `GET /api/reports?status=OPEN&q=`: 관리자가 신고 목록을 조회합니다. `q`는 사유의 키워드로 LIKE 부분 일치 검색합니다.
3. `PATCH /api/reports/{id}`: 관리자가 `{status: ACCEPTED | REJECTED}`로 처리합니다. ACCEPTED면 글을 숨깁니다.
4. 회원 역할은 `MEMBER`와 `ADMIN`입니다.
5. 화면: ADMIN 회원을 선택했을 때만 신고 관리 탭을 보여 주고, OPEN 신고 목록, 키워드 검색, 승인·반려 버튼을 둡니다.

## 수용 기준

* Given 글이 있을 때 / When 회원이 신고하면 / Then 201과 OPEN 상태 신고를 반환합니다
* Given 같은 회원이 같은 글을 신고했을 때 / When 다시 신고하면 / Then 409를 반환합니다
* Given OPEN 신고가 있을 때 / When 관리자가 ACCEPTED로 처리하면 / Then 글이 피드에서 사라집니다
* Given 사유에 "spam"이 들어간 신고가 있을 때 / When `q=spa`로 조회하면 / Then 그 신고가 결과에 포함됩니다

## 범위 밖

* 신고 사유 분류, 처리 이력, 알림
