from sqlalchemy.orm import Session

from app.errors import AppError
from app.follows import repository
from app.members import api as members_api


def follow_member(session: Session, member_id: int, target_id: int) -> None:
    if member_id == target_id:
        raise AppError(400, "INVALID_TARGET", "You cannot follow yourself.")
    if not members_api.member_exists(session, target_id):
        raise AppError(404, "MEMBER_NOT_FOUND", "The target member does not exist.")
    if repository.get_follow(session, member_id, target_id) is not None:
        raise AppError(409, "ALREADY_FOLLOWING", "You already follow that member.")
    repository.create_follow(session, member_id, target_id)


def unfollow_member(session: Session, member_id: int, target_id: int) -> None:
    follow = repository.get_follow(session, member_id, target_id)
    if follow is None:
        raise AppError(404, "FOLLOW_NOT_FOUND", "That follow relationship does not exist.")
    repository.delete_follow(session, follow)


def list_following_members(session: Session, member_id: int) -> list[members_api.MemberOut]:
    if not members_api.member_exists(session, member_id):
        raise AppError(404, "MEMBER_NOT_FOUND", "The member does not exist.")
    return members_api.list_members_by_ids(session, repository.following_ids(session, member_id))


def following_ids(session: Session, member_id: int) -> list[int]:
    return repository.following_ids(session, member_id)
