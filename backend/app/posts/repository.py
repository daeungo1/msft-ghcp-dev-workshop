from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.posts.models import Post


def create_post(session: Session, author_id: int, content: str, created_at: str) -> Post:
    post = Post(author_id=author_id, content=content, created_at=created_at, is_hidden=0)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_post(session: Session, post_id: int) -> Post | None:
    return session.get(Post, post_id)


def list_posts(session: Session, author_id: int | None, limit: int) -> list[Post]:
    query: Select[tuple[Post]] = select(Post).where(Post.is_hidden == 0)
    if author_id is not None:
        query = query.where(Post.author_id == author_id)
    query = query.order_by(Post.id.desc()).limit(limit)
    return list(session.scalars(query))


def list_feed_posts(
    session: Session,
    author_ids: list[int],
    limit: int,
    before: int | None = None,
) -> list[Post]:
    query: Select[tuple[Post]] = select(Post).where(Post.author_id.in_(author_ids), Post.is_hidden == 0)
    if before is not None:
        query = query.where(Post.id < before)
    query = query.order_by(Post.id.desc()).limit(limit)
    return list(session.scalars(query))


def hide_post(session: Session, post_id: int) -> None:
    post = session.get(Post, post_id)
    if post is not None:
        post.is_hidden = 1
