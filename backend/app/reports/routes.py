from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db import get_session
from app.reports import api
from app.reports.schemas import ReportCreate, ReportUpdate
from app.security import current_member_id, require_admin

router = APIRouter(tags=["reports"])


@router.post("/api/posts/{post_id}/reports", response_model=api.ReportOut, status_code=status.HTTP_201_CREATED)
def create_report(
    post_id: int,
    payload: ReportCreate,
    session: Session = Depends(get_session),
    member_id: int = Depends(current_member_id),
) -> api.ReportOut:
    return api.create_report(session, post_id, member_id, payload.reason)


@router.get("/api/reports", response_model=list[api.ReportOut])
def list_reports(
    status_filter: str = Query("OPEN", alias="status"),
    query: str | None = Query(None, alias="q"),
    session: Session = Depends(get_session),
    _: int = Depends(require_admin),
) -> list[api.ReportOut]:
    return api.list_reports(session, status_filter, query)


@router.patch("/api/reports/{report_id}", response_model=api.ReportOut)
def update_report(
    report_id: int,
    payload: ReportUpdate,
    session: Session = Depends(get_session),
    _: int = Depends(require_admin),
) -> api.ReportOut:
    return api.update_report(session, report_id, payload.status)
