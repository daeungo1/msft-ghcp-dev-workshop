from fastapi.testclient import TestClient


def test_create_member_returns_member_payload(client: TestClient) -> None:
    response = client.post("/api/members", json={"name": "alice"})

    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "alice", "role": "MEMBER"}


def test_duplicate_member_name_returns_conflict(client: TestClient) -> None:
    client.post("/api/members", json={"name": "alice"})

    response = client.post("/api/members", json={"name": "alice"})

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "DUPLICATE_NAME"


def test_list_members_returns_created_members(client: TestClient) -> None:
    client.post("/api/members", json={"name": "alice"})
    client.post("/api/members", json={"name": "bob"})

    response = client.get("/api/members")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "alice", "role": "MEMBER"},
        {"id": 2, "name": "bob", "role": "MEMBER"},
    ]


def test_create_member_validates_name_length(client: TestClient) -> None:
    response = client.post("/api/members", json={"name": ""})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
