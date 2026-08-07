from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Topic(Base):

    __tablename__ = "topics"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # Many-to-many relationship with papers
    papers = relationship(
        "Paper",
        secondary="paper_topics",
        back_populates="topics"
    )