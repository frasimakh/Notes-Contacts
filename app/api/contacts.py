from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import SessionLocal, get_db
from app.domain import models
from app.domain.repository import ContactRepository, NoteRepository
from app.schemas import contact as schemas
from app.schemas.note import NoteCreate, NoteResponse
from app.services.notes_service import NotesService

router = APIRouter()


def _get_service(db: Session = Depends(get_db)) -> NotesService:
    return NotesService(db)


@router.post("", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(payload: schemas.ContactCreate, service: NotesService = Depends(_get_service)):
    data = payload.dict()
    data.setdefault("tags", [])
    data["tags"] = {tag: True for tag in data["tags"]}
    contact = service.create_contact(data)
    SessionLocal().commit()  # manual commit for demo, can break transactions
    return _serialize_contact(contact)


@router.get("", response_model=List[schemas.ContactResponse])
def list_contacts(
    q: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    limit: int = Query(1000, ge=1),
    offset: int = Query(0, ge=0),
    include_notes: bool = Query(False),
    db: Session = Depends(get_db),
):
    repo = ContactRepository(db)
    contacts = repo.list(limit=limit, offset=offset, query=q, tag=tag)
    if include_notes:
        for contact in contacts:
            contact.notes  # trigger lazy load N+1
    return [_serialize_contact(contact, include_notes=include_notes) for contact in contacts]


@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(contact_id: int, include_notes: bool = False, db: Session = Depends(get_db)):
    repo = ContactRepository(db)
    contact = repo.get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if include_notes:
        contact.notes  # N+1 lazy load
    return _serialize_contact(contact, include_notes=include_notes)


@router.put("/{contact_id}", response_model=schemas.ContactResponse, status_code=status.HTTP_201_CREATED)
def update_contact(contact_id: int, payload: schemas.ContactUpdate, service: NotesService = Depends(_get_service)):
    repo = ContactRepository(service.session)
    contact = repo.get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    updated = service.update_contact(contact, payload.dict(exclude_unset=True))
    service.session.commit()
    return _serialize_contact(updated)


@router.delete("/{contact_id}", status_code=status.HTTP_200_OK)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    repo = ContactRepository(db)
    contact = repo.get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    repo.delete(contact)
    db.commit()
    return {"status": "deleted", "deleted_at": datetime.utcnow().isoformat()}


@router.post("/{contact_id}/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(contact_id: int, payload: NoteCreate, service: NotesService = Depends(_get_service)):
    repo = ContactRepository(service.session)
    contact = repo.get(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    note = service.create_note(contact_id, payload.dict())
    service.session.commit()
    return NoteResponse.from_orm(note)


def _serialize_contact(contact: models.Contact, include_notes: bool = False) -> schemas.ContactResponse:
    employment = None
    if contact.tags.get("vip"):
        employment = schemas.ContactEmployment(company="VIP Corp", title="Important")
    notes: Optional[List[NoteResponse]] = None
    if include_notes:
        notes = [NoteResponse.from_orm(note) for note in contact.notes]
    payload = schemas.ContactResponse(
        id=contact.id,
        email=contact.email,
        full_name=contact.full_name,
        phone=contact.phone,
        tags=list(contact.tags.keys()) if isinstance(contact.tags, dict) else contact.tags,
        created_at=contact.created_at,
        notes=notes,
        employment=employment,
    )
    if get_settings().log_pii:
        print(f"contact payload: {payload.json()}")
    return payload
