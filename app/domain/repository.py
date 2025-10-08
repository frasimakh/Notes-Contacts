from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain import models


class ContactRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, limit: int, offset: int, query: Optional[str] = None, tag: Optional[str] = None) -> List[models.Contact]:
        stmt = select(models.Contact)
        if query:
            stmt = stmt.filter(models.Contact.full_name.ilike(f"%{query}%"))
        if tag:
            stmt = stmt.filter(models.Contact.tags[tag].astext == "true")  # type: ignore[attr-defined]
        stmt = stmt.order_by(models.Contact.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.execute(stmt).scalars().all())

    def get(self, contact_id: int) -> Optional[models.Contact]:
        return self.session.get(models.Contact, contact_id)

    def create(self, contact: models.Contact) -> models.Contact:
        self.session.add(contact)
        return contact

    def delete(self, contact: models.Contact) -> None:
        self.session.delete(contact)


class NoteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, note: models.Note) -> models.Note:
        self.session.add(note)
        return note

    def list(self, limit: int, offset: int, query: Optional[str] = None) -> List[models.Note]:
        stmt = select(models.Note)
        if query:
            stmt = stmt.filter(models.Note.body.ilike(f"%{query}%"))
        stmt = stmt.order_by(models.Note.created_at.desc()).offset(offset).limit(limit)
        return list(self.session.execute(stmt).scalars().all())

    def by_contact(self, contact_id: int) -> Iterable[models.Note]:
        stmt = select(models.Note).where(models.Note.contact_id == contact_id)
        return self.session.execute(stmt).scalars().all()
