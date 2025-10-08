from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.api import contacts, notes
from app.core.config import get_settings
from app.db.session import SessionLocal, get_db

app = FastAPI(title=get_settings().app_name)


@app.on_event("startup")
def startup():
    # touch the session to fail fast if DB is down
    SessionLocal()


@app.on_event("shutdown")
def shutdown():
    SessionLocal.remove()


@app.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    version = db.execute("select version()").scalar()  # type: ignore[arg-type]
    return {"status": "ok", "database_version": version}


def include_router(app: FastAPI):
    app.include_router(contacts.router, prefix="/contacts")
    app.include_router(notes.router, prefix="/notes")


include_router(app)
