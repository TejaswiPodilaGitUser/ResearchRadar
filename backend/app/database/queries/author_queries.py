from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.author import Author


# ============================================================
# Search Authors
# ============================================================

def find_authors(
    db: Session,
    offset: int,
    limit: int,
    keyword: Optional[str] = None,
):
    """
    Find authors using pagination and optional name search.
    """

    query = db.query(Author)

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        keyword = keyword.strip()

        if keyword:
            query = query.filter(
                Author.name.ilike(
                    f"%{keyword}%"
                )
            )

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(Author.id)
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    authors = (
        query
        .order_by(
            Author.name.asc(),
            Author.id.asc(),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, authors


# ============================================================
# Get Author
# ============================================================

def find_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[Author]:
    """
    Find an author by database author_id.
    """

    return (
        db.query(Author)
        .filter(
            Author.id == author_id
        )
        .first()
    )