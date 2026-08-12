from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Table,
)

from app.database.base import Base


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