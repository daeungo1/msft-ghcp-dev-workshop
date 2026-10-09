from fastapi.testclient import TestClient

from app.posts.models import Post
from tests.conftest import h, make_member


def _post(client: TestClient, member_id: int, content: str) -> dict[str, object]:
    response = client.post("/api/posts", headers=h(member_id), json={"content": content})
    assert response.status_code == 201
    return response.json()


def test_feed_returns_own_and_followed_posts_only(client: TestClient) -> None:
    alice = make_member(client, "alice")
    bob = make_member(client, "bob")
    carol = make_member(client, "carol")
    client.post(f"/api/follows/{bob['id']}", headers=h(alice["id"]))
    _post(client, alice["id"], "from alice")
    _post(client, bob["id"], "from bob")
    _post(client, carol["id"], "from carol")

    response = client.get("/api/feed", headers=h(alice["id"]))

    assert response.status_code == 200
    assert [item["content"] for item in response.json()["items"]] == ["from bob", "from alice"]
    assert response.json()["next_before"] is None


def test_feed_pagination_uses_before_cursor(client: TestClient) -> None:
    alice = make_member(client, "alice")
    bob = make_member(client, "bob")
    client.post(f"/api/follows/{bob['id']}", headers=h(alice["id"]))
    for index in range(25):
        author_id = alice["id"] if index % 2 == 0 else bob["id"]
        _post(client, author_id, f"post {index}")

    first_page = client.get("/api/feed?limit=20", headers=h(alice["id"]))

    assert first_page.status_code == 200
    assert len(first_page.json()["items"]) == 20
    assert first_page.json()["next_before"] == first_page.json()["items"][-1]["id"]

    second_page = client.get(
        f"/api/feed?limit=20&before={first_page.json()['next_before']}",
        headers=h(alice["id"]),
    )

    assert second_page.status_code == 200
    assert len(second_page.json()["items"]) == 5
    assert second_page.json()["next_before"] is None


def test_hidden_posts_are_excluded_from_feed(client: TestClient) -> None:
    alice = make_member(client, "alice")
    bob = make_member(client, "bob")
    client.post(f"/api/follows/{bob['id']}", headers=h(alice["id"]))
    visible = _post(client, bob["id"], "visible")
    hidden = _post(client, bob["id"], "hidden")
    with client.app.state.sessionmaker() as session:
        post = session.get(Post, hidden["id"])
        assert post is not None
        post.is_hidden = 1
        session.commit()

    response = client.get("/api/feed", headers=h(alice["id"]))

    assert response.status_code == 200
    assert [item["id"] for item in response.json()["items"]] == [visible["id"]]
