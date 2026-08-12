from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    Table,
)

from app.database.base import Base


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