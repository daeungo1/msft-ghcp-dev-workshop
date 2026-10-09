from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.reports.models import Report


def add_report(
    session: Session,
    post_id: int,
    reporter_id: int,
    reason: str,
    created_at: str,
) -> Report:
    report = Report(
        post_id=post_id,
        reporter_id=reporter_id,
        reason=reason,
        status="OPEN",
        created_at=created_at,
    )
    session.add(report)
    session.flush()
    return report


def get_report(session: Session, report_id: int) -> Report | None:
    return session.get(Report, report_id)


def find_report(session: Session, post_id: int, reporter_id: int) -> Report | None:
    return session.scalar(
        select(Report).where(Report.post_id == post_id, Report.reporter_id == reporter_id)
    )


def list_reports(session: Session, status: str, query: str | None) -> list[Report]:
    statement: Select[tuple[Report]] = select(Report).where(Report.status == status).order_by(Report.id)
    if query:
        statement = statement.where(Report.reason.ilike(f"%{query}%"))
    return list(session.scalars(statement))
