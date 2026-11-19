from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()

    try:
        yield db
        #This temporarily provides the database session to the FastAPI endpoint.

    finally:
        db.close()