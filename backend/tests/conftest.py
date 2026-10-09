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
