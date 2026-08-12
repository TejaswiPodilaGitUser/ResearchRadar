from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from app.core.config import settings


# ============================================================
# Engine
# ============================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)


# ============================================================
# Session
# ============================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ============================================================
# Dependency
# ============================================================

def get_db():
    """
    Provide database session to API request.
    """

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()