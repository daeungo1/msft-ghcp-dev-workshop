from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.posts import api
from app.posts.schemas import PostCreate
from app.security import current_member_id

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("", response_model=api.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(
    payload: PostCreate,
    session: Session = Depends(get_session),
    member_id: int = Depends(current_member_id),
) -> api.PostOut:
    return api.create_post(session, member_id, payload.content)


@router.get("", response_model=list[api.PostOut])
def list_posts(
    author_id: int | None = None,
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
    _: int = Depends(current_member_id),
) -> list[api.PostOut]:
    return api.list_posts(session, author_id, limit)
