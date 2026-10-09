---
title: 02 팔로우
description: S2 요건. 팔로우, 언팔로우, 팔로잉 목록
---

## 배경

구성원은 관심 있는 동료를 팔로우해 그 사람의 글을 피드에서 받아 봅니다.

## 기능 요건

1. `POST /api/follows/{target_id}`: 대상 회원을 팔로우합니다.
2. `DELETE /api/follows/{target_id}`: 팔로우를 취소합니다.
3. `GET /api/members/{id}/following`: 팔로잉 목록을 조회합니다.
4. 화면: 글 목록의 작성자 옆에 팔로우·언팔로우 버튼을 둡니다.

## 수용 기준

* Given 대상 회원이 있을 때 / When 팔로우하면 / Then 201을 반환하고 팔로잉 목록에 나타납니다
* Given 자기 자신일 때 / When 팔로우하면 / Then 400을 반환합니다
* Given 이미 팔로우했을 때 / When 다시 팔로우하면 / Then 409를 반환합니다
* Given 대상 회원이 없을 때 / When 팔로우하면 / Then 404를 반환합니다
* Given 팔로우하지 않았을 때 / When 언팔로우하면 / Then 404를 반환합니다

## 범위 밖

* 팔로워 목록, 팔로우 추천
