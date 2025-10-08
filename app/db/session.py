from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, pool_size=settings.db_pool_size)
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def get_db() -> Iterator[SessionLocal]:  # type: ignore[valid-type]
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
