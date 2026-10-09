from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.posts import repository
from app.posts.schemas import PostOut


def create_post(session: Session, author_id: int, content: str) -> PostOut:
    created_at = datetime.now(timezone.utc).isoformat()
    post = repository.create_post(session, author_id, content, created_at)
    return PostOut.model_validate(post)


def list_posts(session: Session, author_id: int | None, limit: int) -> list[PostOut]:
    return [PostOut.model_validate(post) for post in repository.list_posts(session, author_id, limit)]


def get_post(session: Session, post_id: int) -> PostOut | None:
    post = repository.get_post(session, post_id)
    return None if post is None else PostOut.model_validate(post)


def list_feed_posts(
    session: Session,
    author_ids: list[int],
    limit: int,
    before: int | None = None,
) -> list[PostOut]:
    return [
        PostOut.model_validate(post)
        for post in repository.list_feed_posts(session, author_ids, limit, before)
    ]


def hide_post(session: Session, post_id: int) -> None:
    repository.hide_post(session, post_id)
