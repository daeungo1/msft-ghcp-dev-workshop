from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Follow(Base):
    __tablename__ = "follows"

    follower_id: Mapped[int] = mapped_column(
        "follower_member_id",
        ForeignKey("members.id"),
        primary_key=True,
    )
    followee_id: Mapped[int] = mapped_column(
        "followee_member_id",
        ForeignKey("members.id"),
        primary_key=True,
    )
