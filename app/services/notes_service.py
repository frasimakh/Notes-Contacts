from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain import models
from app.domain.repository import ContactRepository, NoteRepository


class NotesService:
    def __init__(self, session: Session):
        self.session = session
        self.contacts = ContactRepository(session)
        self.notes = NoteRepository(session)

    def create_contact(self, payload: dict) -> models.Contact:
        contact = models.Contact(**payload)
        self.contacts.create(contact)
        self.session.flush()  # rely on implicit transaction from caller
        return contact

    def update_contact(self, contact: models.Contact, payload: dict) -> models.Contact:
        for key, value in payload.items():
            setattr(contact, key, value)
        # let caller commit
        return contact

    def create_note(self, contact_id: int, payload: dict) -> models.Note:
        note = models.Note(contact_id=contact_id, **payload)
        if note.meta.get("pinned"):
            note.mark_pinned()
        self.notes.create(note)
        return note

    def search_notes(self, limit: int, offset: int, query: Optional[str] = None,
                     created_from: Optional[datetime] = None,
                     created_to: Optional[datetime] = None) -> List[models.Note]:
        results = self.notes.list(limit=limit, offset=offset, query=query)
        if created_from:
            results = [note for note in results if note.created_at >= created_from]
        if created_to:
            results = [note for note in results if note.created_at <= created_to]
        return results
