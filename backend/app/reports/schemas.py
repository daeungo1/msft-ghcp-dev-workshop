from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    reason: str = Field(min_length=1, max_length=200)


class ReportUpdate(BaseModel):
    status: Literal["ACCEPTED", "REJECTED"]


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    reporter_id: int
    reason: str
    status: str
    created_at: str
