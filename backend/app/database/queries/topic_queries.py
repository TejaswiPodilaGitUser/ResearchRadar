from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload

from app.models.topic import Topic


# ============================================================
# Search Topics
# ============================================================

def find_topics(
    db: Session,
    offset: int,
    limit: int,
    keyword: Optional[str] = None,
):
    """
    Find topics using pagination and optional
    name / topic ID search.

    Supports:
        - Single topic ID
        - Multiple comma-separated topic IDs
        - Single topic name
        - Multiple comma-separated topic names
        - Mixed IDs and names
    """

    query = db.query(Topic)

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        keyword = keyword.strip()

        if keyword:

            search_values = [
                value.strip()
                for value in keyword.split(",")
                if value.strip()
            ]

            conditions = []

            for value in search_values:

                # ------------------------------------------------
                # Topic ID
                # ------------------------------------------------

                if value.isdigit():

                    conditions.append(
                        Topic.id == int(value)
                    )

                # ------------------------------------------------
                # Topic Name
                # ------------------------------------------------

                else:

                    conditions.append(
                        Topic.name.ilike(
                            f"%{value}%"
                        )
                    )

            if conditions:
                query = query.filter(
                    or_(*conditions)
                )

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(Topic.id)
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    topics = (
        query
        .order_by(
            Topic.name.asc(),
            Topic.id.asc(),
        )
        .offset(offset)
        .limit(limit)
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
    """
    Find a topic by database ID.

    Also loads all papers associated with
    the topic through the Topic.papers relationship.
    """

    return (
        db.query(Topic)
        .options(
            selectinload(
                Topic.papers
            )
        )
        .filter(
            Topic.id == topic_id
        )
        .first()
    )


# ============================================================
# Get Multiple Topics By IDs
# ============================================================

def find_topics_by_ids(
    db: Session,
    topic_ids: List[int],
) -> List[Topic]:
    """
    Find multiple topics by database IDs.

    Results preserve the order supplied by topic_ids.
    """

    if not topic_ids:
        return []

    unique_ids = list(
        dict.fromkeys(topic_ids)
    )

    topics = (
        db.query(Topic)
        .filter(
            Topic.id.in_(unique_ids)
        )
        .all()
    )

    topics_by_id = {
        topic.id: topic
        for topic in topics
    }

    return [
        topics_by_id[topic_id]
        for topic_id in unique_ids
        if topic_id in topics_by_id
    ]


# ============================================================
# Get Multiple Topics By Names
# ============================================================

def find_topics_by_names(
    db: Session,
    names: List[str],
) -> List[Topic]:
    """
    Find multiple topics by exact names.

    Matching is case-insensitive.
    """

    if not names:
        return []

    normalized_names = [
        name.strip()
        for name in names
        if name and name.strip()
    ]

    if not normalized_names:
        return []

    normalized_lookup = [
        name.casefold()
        for name in normalized_names
    ]

    return (
        db.query(Topic)
        .filter(
            func.lower(
                Topic.name
            ).in_(
                normalized_lookup
            )
        )
        .all()
    )
