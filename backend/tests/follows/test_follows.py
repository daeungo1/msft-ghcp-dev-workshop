from fastapi.testclient import TestClient

from tests.conftest import h, make_member


def test_follow_member_and_list_following(client: TestClient) -> None:
    me = make_member(client, "alice")
    target = make_member(client, "bob")

    response = client.post(f"/api/follows/{target['id']}", headers=h(me["id"]))

    assert response.status_code == 201
    following_response = client.get(f"/api/members/{me['id']}/following", headers=h(me["id"]))
    assert following_response.status_code == 200
    assert following_response.json() == [target]


def test_follow_self_returns_invalid_target(client: TestClient) -> None:
    me = make_member(client, "alice")

    response = client.post(f"/api/follows/{me['id']}", headers=h(me["id"]))

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "INVALID_TARGET"


def test_duplicate_follow_returns_conflict(client: TestClient) -> None:
    me = make_member(client, "alice")
    target = make_member(client, "bob")
    client.post(f"/api/follows/{target['id']}", headers=h(me["id"]))

    response = client.post(f"/api/follows/{target['id']}", headers=h(me["id"]))

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ALREADY_FOLLOWING"


def test_follow_unknown_member_returns_not_found(client: TestClient) -> None:
    me = make_member(client, "alice")

    response = client.post("/api/follows/999", headers=h(me["id"]))

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "MEMBER_NOT_FOUND"


def test_unfollow_missing_relationship_returns_not_found(client: TestClient) -> None:
    me = make_member(client, "alice")
    target = make_member(client, "bob")

    response = client.delete(f"/api/follows/{target['id']}", headers=h(me["id"]))

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "FOLLOW_NOT_FOUND"
