from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    Integer,
    Date,
    DateTime,
    Table,
    ForeignKey,
    Index,
)

from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector

from app.database.database import Base


# ============================================================
# Paper - Author Association Table
# ============================================================

paper_authors = Table(
    "paper_authors",
    Base.metadata,

    Column(
        "paper_id",
        BigInteger,
        ForeignKey(
            "papers.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),

    Column(
        "author_id",
        BigInteger,
        ForeignKey(
            "authors.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)


# ============================================================
# Paper - Topic Association Table
# ============================================================

paper_topics = Table(
    "paper_topics",
    Base.metadata,

    Column(
        "paper_id",
        BigInteger,
        ForeignKey(
            "papers.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),

    Column(
        "topic_id",
        BigInteger,
        ForeignKey(
            "topics.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    ),
)


# ============================================================
# Paper Entity
# ============================================================

class Paper(Base):

    __tablename__ = "papers"

    # --------------------------------------------------------
    # Primary Key
    # --------------------------------------------------------

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    # --------------------------------------------------------
    # OpenAlex ID
    # --------------------------------------------------------

    openalex_id = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    # --------------------------------------------------------
    # Paper Information
    # --------------------------------------------------------

    title = Column(
        Text,
        nullable=False,
        index=True,
    )

    abstract = Column(
        Text,
        nullable=True,
    )

    publication_year = Column(
        Integer,
        nullable=True,
        index=True,
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

    # --------------------------------------------------------
    # AI Embedding
    #
    # all-MiniLM-L6-v2 produces 384-dimensional vectors.
    #
    # PostgreSQL:
    # embedding vector(384)
    # --------------------------------------------------------

    embedding = Column(
        Vector(384),
        nullable=True,
    )

    # --------------------------------------------------------
    # Audit Fields
    # --------------------------------------------------------

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

    def __repr__(self):

        return (
            f"<Paper("
            f"id={self.id}, "
            f"title='{self.title[:50] if self.title else ''}'"
            f")>"
        )


# ============================================================
# Indexes
# ============================================================

Index(
    "idx_paper_title",
    Paper.title,
)

Index(
    "idx_paper_year",
    Paper.publication_year,
)