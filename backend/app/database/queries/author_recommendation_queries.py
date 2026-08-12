from typing import List

from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.author import Author


# ============================================================
# Find Papers By Same Authors
# ============================================================

def find_papers_by_same_authors(
    db: Session,
    paper_id: int,
    author_ids: List[int],
    limit: int,
) -> List[Paper]:
    """
    Find papers sharing one or more authors
    with the source paper.

    Excludes the source paper itself.
    """

    if not author_ids:
        return []

    return (
        db.query(Paper)
        .join(Paper.authors)
        .filter(
            Paper.id != paper_id,
            Author.id.in_(author_ids),
        )
        .distinct()
        .order_by(
            Paper.cited_by_count.desc(),
            Paper.publication_year.desc(),
            Paper.id.desc(),
        )
        .limit(limit)
        .all()
    )