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
    Index
)

from sqlalchemy.orm import relationship

from datetime import datetime, timezone

from app.database.database import Base



# ==========================================
# Paper - Author Association Table
# ==========================================

paper_authors = Table(

    "paper_authors",

    Base.metadata,

    Column(
        "paper_id",
        BigInteger,
        ForeignKey(
            "papers.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),


    Column(
        "author_id",
        BigInteger,
        ForeignKey(
            "authors.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)



# ==========================================
# Paper - Topic Association Table
# ==========================================

paper_topics = Table(

    "paper_topics",

    Base.metadata,


    Column(
        "paper_id",
        BigInteger,
        ForeignKey(
            "papers.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),


    Column(
        "topic_id",
        BigInteger,
        ForeignKey(
            "topics.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)




# ==========================================
# Paper Entity
# ==========================================


class Paper(Base):

    __tablename__ = "papers"



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



    title = Column(

        Text,

        nullable=False,

        index=True
    )



    abstract = Column(

        Text,

        nullable=True
    )



    publication_year = Column(

        Integer,

        index=True
    )



    publication_date = Column(

        Date,

        nullable=True
    )



    doi = Column(

        String(255),

        nullable=True
    )



    cited_by_count = Column(

        Integer,

        default=0
    )



    created_at = Column(

        DateTime,

        default=lambda:
            datetime.now(timezone.utc)
    )



    updated_at = Column(

        DateTime,

        default=lambda:
            datetime.now(timezone.utc),

        onupdate=lambda:
            datetime.now(timezone.utc)
    )



    # ======================================
    # Relationships
    # ======================================


    authors = relationship(

        "Author",

        secondary=paper_authors,

        back_populates="papers",

        lazy="joined"
    )



    topics = relationship(

        "Topic",

        secondary=paper_topics,

        back_populates="papers",

        lazy="joined"
    )



    def __repr__(self):

        return (
            f"<Paper(id={self.id}, "
            f"title='{self.title[:50]}')>"
        )



# ==========================================
# Indexes
# ==========================================

Index(
    "idx_paper_title",
    Paper.title
)


Index(
    "idx_paper_year",
    Paper.publication_year
)