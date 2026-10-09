from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.db import get_session
from app.errors import forbidden, unauthenticated
from app.members import api as members_api


def current_member_id(request: Request, session: Session = Depends(get_session)) -> int:
    raw_member_id = request.headers.get("X-Member-Id")
    if raw_member_id is None:
        raise unauthenticated("X-Member-Id header is required.")
    try:
        member_id = int(raw_member_id)
    except ValueError as exc:
        raise unauthenticated("X-Member-Id header is invalid.") from exc
    if member_id <= 0 or not members_api.member_exists(session, member_id):
        raise unauthenticated("X-Member-Id header is invalid.")
    return member_id


def require_admin(
    member_id: int = Depends(current_member_id),
    session: Session = Depends(get_session),
) -> int:
    if members_api.get_role(session, member_id) != "ADMIN":
        raise forbidden("Admin access is required.")
    return member_id
