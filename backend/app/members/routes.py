from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.members import api
from app.members.schemas import MemberCreate

router = APIRouter(prefix="/api/members", tags=["members"])


@router.post("", response_model=api.MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, session: Session = Depends(get_session)) -> api.MemberOut:
    return api.create_member(session, payload.name)


@router.get("", response_model=list[api.MemberOut])
def list_members(session: Session = Depends(get_session)) -> list[api.MemberOut]:
    return api.list_members(session)
