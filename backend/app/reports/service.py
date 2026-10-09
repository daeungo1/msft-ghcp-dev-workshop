from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.errors import AppError
from app.posts import api as posts_api
from app.reports import repository
from app.reports.schemas import ReportOut


def create_report(session: Session, post_id: int, reporter_id: int, reason: str) -> ReportOut:
    if posts_api.get_post(session, post_id) is None:
        raise AppError(404, "POST_NOT_FOUND", "The post does not exist.")
    if repository.find_report(session, post_id, reporter_id) is not None:
        raise AppError(409, "REPORT_ALREADY_EXISTS", "You already reported that post.")
    report = repository.add_report(
        session,
        post_id,
        reporter_id,
        reason,
        datetime.now(timezone.utc).isoformat(),
    )
    session.commit()
    session.refresh(report)
    return ReportOut.model_validate(report)


def list_reports(session: Session, status: str, query: str | None) -> list[ReportOut]:
    return [ReportOut.model_validate(report) for report in repository.list_reports(session, status, query)]


def update_report(session: Session, report_id: int, status: str) -> ReportOut:
    report = repository.get_report(session, report_id)
    if report is None:
        raise AppError(404, "REPORT_NOT_FOUND", "The report does not exist.")
    if report.status != "OPEN":
        raise AppError(409, "INVALID_REPORT_STATUS", "Only OPEN reports can be processed.")
    report.status = status
    if status == "ACCEPTED":
        posts_api.hide_post(session, report.post_id)
    session.commit()
    session.refresh(report)
    return ReportOut.model_validate(report)
