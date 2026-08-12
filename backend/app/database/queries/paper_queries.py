from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic


# ============================================================
# Search Papers
# ============================================================

def find_papers(
    db: Session,
    offset: int,
    limit: int,
    keyword: Optional[str] = None,
    year: Optional[int] = None,
    topic: Optional[str] = None,
    author: Optional[str] = None,
):
    """
    Find papers using optional filters.

    Database responsibility only.
    """

    query = db.query(Paper)

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        search_text = f"%{keyword.strip()}%"

        query = query.filter(
            or_(
                Paper.title.ilike(search_text),
                Paper.abstract.ilike(search_text),
            )
        )

    # --------------------------------------------------------
    # Publication year
    # --------------------------------------------------------

    if year is not None:
        query = query.filter(
            Paper.publication_year == year
        )

    # --------------------------------------------------------
    # Topic
    # --------------------------------------------------------

    if topic:
        query = (
            query
            .join(Paper.topics)
            .filter(
                Topic.name.ilike(
                    f"%{topic.strip()}%"
                )
            )
        )

    # --------------------------------------------------------
    # Author
    # --------------------------------------------------------

    if author:
        query = (
            query
            .join(Paper.authors)
            .filter(
                Author.name.ilike(
                    f"%{author.strip()}%"
                )
            )
        )

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(
                func.distinct(Paper.id)
            )
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    papers = (
        query
        .distinct()
        .order_by(
            Paper.publication_year.desc(),
            Paper.id.desc(),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, papers


# ============================================================
# Get Paper By ID
# ============================================================

def find_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[Paper]:
    """
    Find a paper by database ID.
    """

    return (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )