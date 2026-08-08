from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.topic import Topic


def search_topics(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
):
    """
    Search and paginate topics.
    """

    page = (
        page
        if page is not None
        else settings.DEFAULT_PAGE
    )

    size = (
        size
        if size is not None
        else settings.DEFAULT_PAGE_SIZE
    )

    page = max(
        page,
        settings.DEFAULT_PAGE,
    )

    size = max(
        1,
        min(
            size,
            settings.MAX_PAGE_SIZE,
        ),
    )

    query = db.query(Topic)

    if keyword:
        keyword = keyword.strip()

        if keyword:
            query = query.filter(
                Topic.name.ilike(
                    f"%{keyword}%"
                )
            )

    total = (
        query
        .with_entities(
            func.count(Topic.id)
        )
        .scalar()
    ) or 0

    offset = (page - 1) * size

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

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": topics,
    }


def get_topic_by_id(
    db: Session,
    topic_id: int,
) -> Optional[Topic]:
    """
    Get topic including associated papers.
    """

    return (
        db.query(Topic)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )
