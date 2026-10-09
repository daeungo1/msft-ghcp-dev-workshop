from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (UniqueConstraint("post_id", "reporter_member_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    reporter_id: Mapped[int] = mapped_column("reporter_member_id", ForeignKey("members.id"))
    reason: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(20), default="OPEN")
    created_at: Mapped[str] = mapped_column("created_ts")
