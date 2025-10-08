from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    body: str = Field(min_length=1)
    meta: Dict[str, Any] = Field(default_factory=dict)


class NoteResponse(BaseModel):
    id: int
    contact_id: int
    body: str
    meta: Dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True


class NoteSearchFilters(BaseModel):
    query: Optional[str] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None
