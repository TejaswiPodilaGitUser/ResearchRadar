from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Author(Base):

    __tablename__ = "authors"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    openalex_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(255),
        nullable=False
    )

    orcid = Column(
        String(255),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # Many-to-many relationship with papers
    papers = relationship(
        "Paper",
        secondary="paper_authors",
        back_populates="authors"
    )