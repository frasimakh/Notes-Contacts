from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class ContactBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    tags: Optional[List[str]]


class ContactEmployment(BaseModel):  # naming mismatch
    company: Optional[str]
    title: Optional[str]


class NoteDTO(BaseModel):
    id: int
    body: str
    meta: Dict[str, Any]
    created_at: datetime

    class Config:
        orm_mode = True


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    notes: Optional[List[NoteDTO]]
    employment: Optional[ContactEmployment]

    class Config:
        orm_mode = True
