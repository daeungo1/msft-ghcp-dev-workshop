from fastapi.testclient import TestClient

from tests.conftest import h, make_member


def test_create_post_requires_authentication(client: TestClient) -> None:
    response = client.post("/api/posts", json={"content": "hello"})

    assert response.status_code == 401
    assert response.json() == {
        "error": {"code": "UNAUTHENTICATED", "message": "X-Member-Id header is required."}
    }


def test_create_post_validates_content_length(client: TestClient) -> None:
    member = make_member(client, "alice")

    response = client.post("/api/posts", headers=h(member["id"]), json={"content": "x" * 281})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_create_and_list_posts_newest_first(client: TestClient) -> None:
    member = make_member(client, "alice")
    headers = h(member["id"])
    for content in ("first", "second", "third"):
        response = client.post("/api/posts", headers=headers, json={"content": content})
        assert response.status_code == 201

    response = client.get(f"/api/posts?author_id={member['id']}", headers=headers)

    assert response.status_code == 200
    assert [item["content"] for item in response.json()] == ["third", "second", "first"]
    assert all(item["author_id"] == member["id"] for item in response.json())


def test_list_posts_without_author_filter_returns_all_visible_posts(client: TestClient) -> None:
    alice = make_member(client, "alice")
    bob = make_member(client, "bob")
    client.post("/api/posts", headers=h(alice["id"]), json={"content": "from alice"})
    client.post("/api/posts", headers=h(bob["id"]), json={"content": "from bob"})

    response = client.get("/api/posts", headers=h(alice["id"]))

    assert response.status_code == 200
    assert [item["content"] for item in response.json()] == ["from bob", "from alice"]
