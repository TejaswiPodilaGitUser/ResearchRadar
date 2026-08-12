from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.topic import Topic


# ============================================================
# Search Topics
# ============================================================

def search_topics(
    db: Session,
    page: int,
    size: int,
    keyword: Optional[str] = None,
):
    """
    Search topics with pagination.
    """

    query = db.query(Topic)

    # --------------------------------------------------------
    # Keyword filter
    # --------------------------------------------------------

    if keyword:

        keyword = keyword.strip()

        if keyword:

            query = query.filter(
                Topic.name.ilike(
                    f"%{keyword}%"
                )
            )

    # --------------------------------------------------------
    # Total count
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(Topic.id)
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (
        page - 1
    ) * size

    topics = (
        query
        .order_by(
            Topic.name.asc(),
            Topic.id.asc(),
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    return total, topics


# ============================================================
# Get Topic By ID
# ============================================================

def find_topic_by_id(
    db: Session,
    topic_id: int,
) -> Optional[Topic]:

    return (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )