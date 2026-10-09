from pydantic import BaseModel

from app.posts.api import PostOut


class FeedPage(BaseModel):
    items: list[PostOut]
    next_before: int | None
