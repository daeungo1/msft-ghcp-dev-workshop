from sqlalchemy.orm import Session

from app.feed.schemas import FeedPage
from app.follows import api as follows_api
from app.posts import api as posts_api


def get_feed(session: Session, member_id: int, limit: int, before: int | None) -> FeedPage:
    author_ids = [member_id, *follows_api.following_ids(session, member_id)]
    posts = posts_api.list_feed_posts(session, author_ids, limit, before)
    next_before = posts[-1].id if len(posts) == limit else None
    return FeedPage(items=posts, next_before=next_before)
