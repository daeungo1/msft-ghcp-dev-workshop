import os
from collections.abc import Generator

from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def default_database_url() -> str:
    value = os.environ.get("TEAMFEED_DB", "teamfeed.db")
    if value.startswith("sqlite:"):
        return value
    return f"sqlite:///{value}"


def make_engine(url: str) -> Engine:
    if url == "sqlite://":
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    if url.startswith("sqlite:"):
        return create_engine(url, connect_args={"check_same_thread": False})
    return create_engine(url)


def import_models() -> None:
    import app.follows.models  # noqa: F401
    import app.members.models  # noqa: F401
    import app.posts.models  # noqa: F401
    import app.reports.models  # noqa: F401


def get_session(request: Request) -> Generator[Session, None, None]:
    with request.app.state.sessionmaker() as session:
        yield session
