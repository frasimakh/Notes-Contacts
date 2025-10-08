from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.note import NoteResponse, NoteSearchFilters
from app.services.notes_service import NotesService

router = APIRouter()


@router.get("", response_model=List[NoteResponse])
def search_notes(
    query: Optional[str] = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    limit: int = Query(500, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    service = NotesService(db)
    filters = NoteSearchFilters(query=query, created_from=created_from, created_to=created_to)
    notes = service.search_notes(limit=limit, offset=offset, query=filters.query,
                                 created_from=filters.created_from, created_to=filters.created_to)
    return [NoteResponse.from_orm(note) for note in notes]
