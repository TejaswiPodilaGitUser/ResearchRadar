from sqlalchemy import (
    BigInteger,
    Column,
    String,
)

from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.associations.paper_topic import paper_topics


class Topic(Base):

    __tablename__ = "topics"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(500),
        nullable=False,
        unique=True,
        index=True,
    )

    papers = relationship(
        "Paper",
        secondary=paper_topics,
        back_populates="topics",
        lazy="selectin",
    )

    def __repr__(self):

        return (
            f"<Topic("
            f"id={self.id}, "
            f"name='{self.name}'"
            f")>"
        )