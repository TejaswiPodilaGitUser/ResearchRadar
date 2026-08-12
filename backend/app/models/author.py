from sqlalchemy import (
    BigInteger,
    Column,
    String,
)

from sqlalchemy.orm import relationship

from app.database.base import Base
from app.models.associations.paper_author import paper_authors


class Author(Base):

    __tablename__ = "authors"

    id = Column(
        BigInteger,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(500),
        nullable=False,
        index=True,
    )

    orcid = Column(
        String(100),
        nullable=True,
    )

    papers = relationship(
        "Paper",
        secondary=paper_authors,
        back_populates="authors",
        lazy="selectin",
    )

    def __repr__(self):

        return (
            f"<Author("
            f"id={self.id}, "
            f"name='{self.name}'"
            f")>"
        )