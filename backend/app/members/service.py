from sqlalchemy.orm import Session

from app.errors import AppError
from app.members import repository
from app.members.schemas import MemberOut


def create_member(session: Session, name: str) -> MemberOut:
    if repository.get_member_by_name(session, name) is not None:
        raise AppError(409, "DUPLICATE_NAME", "A member with that name already exists.")
    return MemberOut.model_validate(repository.create_member(session, name))


def list_members(session: Session) -> list[MemberOut]:
    return [MemberOut.model_validate(member) for member in repository.list_members(session)]


def get_member(session: Session, member_id: int) -> MemberOut | None:
    member = repository.get_member(session, member_id)
    return None if member is None else MemberOut.model_validate(member)


def member_exists(session: Session, member_id: int) -> bool:
    return repository.get_member(session, member_id) is not None


def get_role(session: Session, member_id: int) -> str | None:
    member = repository.get_member(session, member_id)
    return None if member is None else member.role
