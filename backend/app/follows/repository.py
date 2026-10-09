from sqlalchemy import select
from sqlalchemy.orm import Session

from app.follows.models import Follow


def create_follow(session: Session, follower_id: int, followee_id: int) -> Follow:
    follow = Follow(follower_id=follower_id, followee_id=followee_id)
    session.add(follow)
    session.commit()
    session.refresh(follow)
    return follow


def get_follow(session: Session, follower_id: int, followee_id: int) -> Follow | None:
    return session.get(Follow, {"follower_id": follower_id, "followee_id": followee_id})


def delete_follow(session: Session, follow: Follow) -> None:
    session.delete(follow)
    session.commit()


def following_ids(session: Session, member_id: int) -> list[int]:
    query = select(Follow.followee_id).where(Follow.follower_id == member_id).order_by(Follow.followee_id)
    return list(session.scalars(query))
