from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import update

from app.main import create_app
from app.members.models import Member


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    app = create_app("sqlite://")
    with TestClient(app) as test_client:
        yield test_client


def h(member_id: int) -> dict[str, str]:
    return {"X-Member-Id": str(member_id)}


def make_member(client: TestClient, name: str, role: str = "MEMBER") -> dict[str, object]:
    response = client.post("/api/members", json={"name": name})
    assert response.status_code == 201
    member = response.json()
    if role != "MEMBER":
        with client.app.state.sessionmaker() as session:
            session.execute(update(Member).where(Member.id == member["id"]).values(role=role))
            session.commit()
        member["role"] = role
    return member


@pytest.fixture
def api_client(client: TestClient) -> TestClient:
    """기본 요청자가 ADMIN 회원인 클라이언트. 다른 사용자로 요청하려면 헤더를 직접 지정한다."""
    admin = make_member(client, "default-admin", role="ADMIN")
    client.headers.update(h(admin["id"]))
    return client