from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    Index,
)

from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector

from app.database.base import Base

from app.models.associations.paper_author import paper_authors
from app.models.associations.paper_topic import paper_topics


# ============================================================
# Paper Model
# ============================================================

class Paper(Base):

    __tablename__ = "papers"

    # ========================================================
    # Primary Key
    # ========================================================

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    # ========================================================
    # OpenAlex
    # ========================================================

    openalex_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # ========================================================
    # Paper Information
    # ========================================================

    title = Column(
        Text,
        nullable=False,
    )

    abstract = Column(
        Text,
        nullable=True,
    )

    publication_year = Column(
        Integer,
        nullable=True,
    )

    publication_date = Column(
        Date,
        nullable=True,
    )

    doi = Column(
        String(255),
        nullable=True,
    )

    cited_by_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    # ========================================================
    # AI Embedding
    #
    # all-MiniLM-L6-v2 -> 384 dimensions
    #
    # PostgreSQL:
    # embedding vector(384)
    # ========================================================

    embedding = Column(
        Vector(384),
        nullable=True,
    )

    # ========================================================
    # Audit Fields
    # ========================================================

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # ========================================================
    # Relationships
    # ========================================================

    authors = relationship(
        "Author",
        secondary=paper_authors,
        back_populates="papers",
        lazy="selectin",
    )

    topics = relationship(
        "Topic",
        secondary=paper_topics,
        back_populates="papers",
        lazy="selectin",
    )

    # ========================================================
    # Representation
    # ========================================================

    def __repr__(self) -> str:

        title = (
            self.title[:50]
            if self.title
            else ""
        )

        return (
            f"<Paper("
            f"id={self.id}, "
            f"title='{title}'"
            f")>"
        )


# ============================================================
# Indexes
# ============================================================

Index(
    "idx_papers_publication_year",
    Paper.publication_year,
)

Index(
    "idx_papers_cited_by_count",
    Paper.cited_by_count,
)