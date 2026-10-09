from sqlalchemy import select
from sqlalchemy.orm import Session

from app.members.models import Member


def create_member(session: Session, name: str) -> Member:
    member = Member(name=name, role="MEMBER")
    session.add(member)
    session.commit()
    session.refresh(member)
    return member


def get_member(session: Session, member_id: int) -> Member | None:
    return session.get(Member, member_id)


def get_member_by_name(session: Session, name: str) -> Member | None:
    return session.scalar(select(Member).where(Member.name == name))


def list_members(session: Session) -> list[Member]:
    return list(session.scalars(select(Member).order_by(Member.id)))


def list_members_by_ids(session: Session, member_ids: list[int]) -> list[Member]:
    if not member_ids:
        return []
    query = select(Member).where(Member.id.in_(member_ids)).order_by(Member.id)
    return list(session.scalars(query))
