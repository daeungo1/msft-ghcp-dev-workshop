from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.follows import api
from app.members import api as members_api
from app.security import current_member_id

router = APIRouter(tags=["follows"])


@router.post("/api/follows/{target_id}", status_code=status.HTTP_201_CREATED)
def follow_member(
    target_id: int,
    session: Session = Depends(get_session),
    member_id: int = Depends(current_member_id),
) -> Response:
    api.follow_member(session, member_id, target_id)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/api/follows/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_member(
    target_id: int,
    session: Session = Depends(get_session),
    member_id: int = Depends(current_member_id),
) -> Response:
    api.unfollow_member(session, member_id, target_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/api/members/{member_id}/following", response_model=list[members_api.MemberOut])
def list_following_members(
    member_id: int,
    session: Session = Depends(get_session),
    _: int = Depends(current_member_id),
) -> list[members_api.MemberOut]:
    return api.list_following_members(session, member_id)
