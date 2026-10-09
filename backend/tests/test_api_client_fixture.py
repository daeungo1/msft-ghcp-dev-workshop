from fastapi.testclient import TestClient


def test_api_client_requests_as_admin(api_client: TestClient) -> None:
    response = api_client.get("/api/feed")
    assert response.status_code == 200