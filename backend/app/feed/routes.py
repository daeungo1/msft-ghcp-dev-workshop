from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db import get_session
from app.feed import api
from app.security import current_member_id

router = APIRouter(prefix="/api/feed", tags=["feed"])


@router.get("", response_model=api.FeedPage)
def get_feed(
    limit: int = Query(20, ge=1, le=100),
    before: int | None = Query(None, ge=1),
    session: Session = Depends(get_session),
    member_id: int = Depends(current_member_id),
) -> api.FeedPage:
    return api.get_feed(session, member_id, limit, before)
