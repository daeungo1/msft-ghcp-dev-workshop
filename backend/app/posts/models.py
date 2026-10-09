from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column("author_member_id", ForeignKey("members.id"))
    content: Mapped[str] = mapped_column("body", String(280))
    created_at: Mapped[str] = mapped_column("created_ts")
    is_hidden: Mapped[int] = mapped_column(default=0)
