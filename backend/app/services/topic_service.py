from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings

from app.database.queries.topic_queries import (
    search_topics as query_search_topics,
    find_topic_by_id,
)

from app.models.topic import Topic


# ============================================================
# Topic Mapping
# ============================================================

def _topic_to_response(
    topic: Topic,
) -> dict:

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
    }


# ============================================================
# Paper Mapping
# ============================================================

def _paper_to_response(
    paper,
) -> dict:

    return {
        "paper_id": paper.id,
        "paper_name": paper.title,
        "publication_year": paper.publication_year,
        "cited_by_count": paper.cited_by_count,
    }


# ============================================================
# Search Topics
# ============================================================

def search_topics(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
):
    """
    Search topics with pagination.
    """

    # --------------------------------------------------------
    # Defaults
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Guardrails
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    total, topics = query_search_topics(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": [
            _topic_to_response(topic)
            for topic in topics
        ],
    }


# ============================================================
# Get Topic By ID
# ============================================================

def get_topic_by_id(
    db: Session,
    topic_id: int,
) -> Optional[dict]:

    topic = find_topic_by_id(
        db=db,
        topic_id=topic_id,
    )

    if topic is None:
        return None

    # --------------------------------------------------------
    # Associated papers
    # --------------------------------------------------------

    papers = [
        _paper_to_response(paper)
        for paper in topic.papers
    ]

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        "papers": papers,
    }