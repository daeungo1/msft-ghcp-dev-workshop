from fastapi.testclient import TestClient

from tests.conftest import h, make_member


def _post(client: TestClient, member_id: int, content: str) -> dict[str, object]:
    response = client.post("/api/posts", headers=h(member_id), json={"content": content})
    assert response.status_code == 201
    return response.json()


def _report(client: TestClient, member_id: int, post_id: int, reason: str) -> dict[str, object]:
    response = client.post(
        f"/api/posts/{post_id}/reports",
        headers=h(member_id),
        json={"reason": reason},
    )
    assert response.status_code == 201
    return response.json()


def test_member_can_report_post(client: TestClient) -> None:
    author = make_member(client, "author")
    reporter = make_member(client, "reporter")
    post = _post(client, author["id"], "report me")

    response = client.post(
        f"/api/posts/{post['id']}/reports",
        headers=h(reporter["id"]),
        json={"reason": "spam content"},
    )

    assert response.status_code == 201
    assert response.json()["status"] == "OPEN"
    assert response.json()["reporter_id"] == reporter["id"]


def test_duplicate_report_returns_conflict(client: TestClient) -> None:
    author = make_member(client, "author")
    reporter = make_member(client, "reporter")
    post = _post(client, author["id"], "report me")
    _report(client, reporter["id"], post["id"], "spam content")

    response = client.post(
        f"/api/posts/{post['id']}/reports",
        headers=h(reporter["id"]),
        json={"reason": "spam content"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "REPORT_ALREADY_EXISTS"


def test_reporting_unknown_post_returns_not_found(client: TestClient) -> None:
    reporter = make_member(client, "reporter")

    response = client.post(
        "/api/posts/999/reports",
        headers=h(reporter["id"]),
        json={"reason": "spam content"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "POST_NOT_FOUND"


def test_reports_search_and_accept_hides_post_from_feed(client: TestClient) -> None:
    admin = make_member(client, "admin", role="ADMIN")
    reporter = make_member(client, "reporter")
    author = make_member(client, "author")
    client.post(f"/api/follows/{author['id']}", headers=h(reporter["id"]))
    post = _post(client, author["id"], "report me")
    report = _report(client, reporter["id"], post["id"], "spam content")

    list_response = client.get("/api/reports?status=OPEN&q=spa", headers=h(admin["id"]))

    assert list_response.status_code == 200
    assert [item["id"] for item in list_response.json()] == [report["id"]]

    patch_response = client.patch(
        f"/api/reports/{report['id']}",
        headers=h(admin["id"]),
        json={"status": "ACCEPTED"},
    )

    assert patch_response.status_code == 200
    feed_response = client.get("/api/feed", headers=h(reporter["id"]))
    assert feed_response.status_code == 200
    assert feed_response.json()["items"] == []


def test_report_endpoints_require_admin(client: TestClient) -> None:
    author = make_member(client, "author")
    admin = make_member(client, "admin", role="ADMIN")
    member = make_member(client, "member")
    post = _post(client, author["id"], "report me")
    report = _report(client, member["id"], post["id"], "spam content")

    list_response = client.get("/api/reports?status=OPEN", headers=h(member["id"]))
    patch_response = client.patch(
        f"/api/reports/{report['id']}",
        headers=h(member["id"]),
        json={"status": "REJECTED"},
    )

    assert list_response.status_code == 403
    assert list_response.json()["error"]["code"] == "FORBIDDEN"
    assert patch_response.status_code == 403
    assert patch_response.json()["error"]["code"] == "FORBIDDEN"

    ok_response = client.get("/api/reports?status=OPEN", headers=h(admin["id"]))
    assert ok_response.status_code == 200


def test_processing_closed_report_returns_conflict(client: TestClient) -> None:
    admin = make_member(client, "admin", role="ADMIN")
    author = make_member(client, "author")
    reporter = make_member(client, "reporter")
    post = _post(client, author["id"], "report me")
    report = _report(client, reporter["id"], post["id"], "spam content")
    client.patch(
        f"/api/reports/{report['id']}",
        headers=h(admin["id"]),
        json={"status": "REJECTED"},
    )

    response = client.patch(
        f"/api/reports/{report['id']}",
        headers=h(admin["id"]),
        json={"status": "ACCEPTED"},
    )

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "INVALID_REPORT_STATUS"
