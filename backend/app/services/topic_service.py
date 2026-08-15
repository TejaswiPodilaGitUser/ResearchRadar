from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException

from app.database.queries.topic_queries import (
    find_topics,
    find_topic_by_id,
    find_topics_by_ids,
    find_topics_by_names,
)


# ============================================================
# Topic Mapping
# ============================================================

def _topic_to_response(
    topic,
) -> dict:
    """
    Convert Topic model to API response.
    """

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
    """
    Convert Paper model to API response.
    """

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
    # Pagination
    # --------------------------------------------------------

    offset = (
        page - 1
    ) * size

    # --------------------------------------------------------
    # Database Query
    # --------------------------------------------------------

    total, topics = find_topics(
        db=db,
        offset=offset,
        limit=size,
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
    """
    Get one topic including associated papers.
    """

    topic = find_topic_by_id(
        db=db,
        topic_id=topic_id,
    )

    if topic is None:
        return None

    papers = [
        _paper_to_response(paper)
        for paper in topic.papers
    ]

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        "papers": papers,
    }


# ============================================================
# Get Topic By Name
# ============================================================

def get_topic_by_name(
    db: Session,
    topic_name: str,
) -> Optional[dict]:
    """
    Get one topic by exact name.

    Matching is case-insensitive.
    """

    topics = find_topics_by_names(
        db=db,
        names=[topic_name],
    )

    if not topics:
        return None

    topic = topics[0]

    papers = [
        _paper_to_response(paper)
        for paper in topic.papers
    ]

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        "papers": papers,
    }


# ============================================================
# Get Multiple Topics By IDs
# ============================================================

def get_multiple_topics(
    db: Session,
    topic_ids: list[int],
):
    """
    Get research information across multiple topics.
    """

    topic_ids = list(
        dict.fromkeys(topic_ids)
    )

    if len(topic_ids) < 2:
        raise ValueError(
            "At least two topic IDs are required."
        )

    topics = find_topics_by_ids(
        db=db,
        topic_ids=topic_ids,
    )

    topics_by_id = {
        topic.id: topic
        for topic in topics
    }

    # --------------------------------------------------------
    # Missing Topics
    # --------------------------------------------------------

    missing_topic_ids = [
        topic_id
        for topic_id in topic_ids
        if topic_id not in topics_by_id
    ]

    if missing_topic_ids:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=", ".join(
                str(topic_id)
                for topic_id in missing_topic_ids
            ),
        )

    # --------------------------------------------------------
    # Preserve Request Order
    # --------------------------------------------------------

    ordered_topics = [
        topics_by_id[topic_id]
        for topic_id in topic_ids
    ]

    return _build_multiple_topic_response(
        topic_ids=topic_ids,
        topics=ordered_topics,
    )


# ============================================================
# Get Multiple Topics By Names
# ============================================================

def get_multiple_topics_by_names(
    db: Session,
    topic_names: list[str],
):
    """
    Get research information across multiple topics
    using exact topic names.

    Matching is case-insensitive.
    """

    # --------------------------------------------------------
    # Clean Names
    # --------------------------------------------------------

    cleaned_names = [
        name.strip()
        for name in topic_names
        if name and name.strip()
    ]

    normalized_names = []
    seen_names = set()

    for name in cleaned_names:
        normalized_name = name.casefold()

        if normalized_name in seen_names:
            continue

        seen_names.add(normalized_name)
        normalized_names.append(name)

    topic_names = normalized_names

    # --------------------------------------------------------
    # Guardrail
    # --------------------------------------------------------

    if len(topic_names) < 2:
        raise ValueError(
            "At least two topic names are required."
        )

    # --------------------------------------------------------
    # Database Query
    # --------------------------------------------------------

    topics = find_topics_by_names(
        db=db,
        names=topic_names,
    )

    topics_by_name = {
        topic.name.strip().casefold(): topic
        for topic in topics
    }

    # --------------------------------------------------------
    # Missing Topics
    # --------------------------------------------------------

    missing_topic_names = [
        name
        for name in topic_names
        if name.strip().casefold()
        not in topics_by_name
    ]

    if missing_topic_names:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=", ".join(
                missing_topic_names
            ),
        )

    # --------------------------------------------------------
    # Preserve Request Order
    # --------------------------------------------------------

    ordered_topics = [
        topics_by_name[
            name.strip().casefold()
        ]
        for name in topic_names
    ]

    topic_ids = [
        topic.id
        for topic in ordered_topics
    ]

    return _build_multiple_topic_response(
        topic_ids=topic_ids,
        topics=ordered_topics,
    )


# ============================================================
# Build Multiple Topic Response
# ============================================================

def _build_multiple_topic_response(
    topic_ids: list[int],
    topics: list,
):
    """
    Build the multiple-topic response.
    """

    topics_by_id = {
        topic.id: topic
        for topic in topics
    }

    # --------------------------------------------------------
    # Topic Details
    # --------------------------------------------------------

    topic_details = [
        _topic_to_response(
            topics_by_id[topic_id]
        )
        for topic_id in topic_ids
    ]

    # --------------------------------------------------------
    # Papers By Topic
    # --------------------------------------------------------

    papers_by_topic = {}

    for topic_id in topic_ids:

        topic = topics_by_id[topic_id]

        papers_by_topic[str(topic_id)] = [
            _paper_to_response(paper)
            for paper in topic.papers
        ]

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "topics": topic_details,
        "papers_by_topic": papers_by_topic,
    }