from typing import List

from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.topic import Topic


# ============================================================
# Find Papers By Same Topics
# ============================================================

def find_papers_by_same_topics(
    db: Session,
    paper_id: int,
    topic_ids: List[int],
    limit: int,
) -> List[Paper]:
    """
    Find papers sharing one or more topics
    with the source paper.

    Excludes the source paper itself.
    """

    if not topic_ids:
        return []

    return (
        db.query(Paper)
        .join(Paper.topics)
        .filter(
            Paper.id != paper_id,
            Topic.id.in_(topic_ids),
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