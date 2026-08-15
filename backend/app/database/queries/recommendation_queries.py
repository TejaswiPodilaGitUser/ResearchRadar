from typing import List, Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.topic import Topic


# ============================================================
# Get Paper By ID
# ============================================================

def get_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[Paper]:
    """
    Get a paper by database ID.
    """

    return (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )


# ============================================================
# Find Similar Papers
# ============================================================

def find_similar_papers(
    db: Session,
    paper: Paper,
    limit: int,
) -> List[Paper]:
    """
    Find papers using semantic similarity.

    Uses pgvector cosine distance.
    """

    if paper.embedding is None:
        return []

    cosine_distance = (
        Paper.embedding.cosine_distance(
            paper.embedding
        )
    )

    return (
        db.query(Paper)
        .filter(
            Paper.embedding.is_not(None),
            Paper.id != paper.id,
        )
        .order_by(
            cosine_distance.asc()
        )
        .limit(limit)
        .all()
    )


# ============================================================
# Trending Papers
# ============================================================

def find_trending_papers(
    db: Session,
    limit: int = 10,
) -> List[Paper]:
    """
    Find top trending research papers.

    Ranking:
        1. Citation count
        2. Publication year
        3. Paper ID
    """

    return (
        db.query(Paper)
        .filter(
            Paper.publication_year.is_not(None),
        )
        .order_by(
            Paper.cited_by_count.desc(),
            Paper.publication_year.desc(),
            Paper.id.desc(),
        )
        .limit(limit)
        .all()
    )


# ============================================================
# Find Emerging Topics
# ============================================================

def find_emerging_topics(
    db: Session,
    limit: int = 10,
):
    """
    Find top emerging research topics.

    Recent activity is based on the latest publication
    year available in the database and the previous year.
    """

    recent_year = (
        db.query(
            func.max(Paper.publication_year)
        )
        .filter(
            Paper.publication_year.is_not(None)
        )
        .scalar()
    )

    if recent_year is None:
        return []

    recent_start_year = recent_year - 1

    recent_paper_count = func.sum(
        func.case(
            (
                Paper.publication_year >= recent_start_year,
                1,
            ),
            else_=0,
        )
    )

    total_paper_count = func.count(
        Paper.id
    )

    citation_count = func.coalesce(
        func.sum(
            Paper.cited_by_count
        ),
        0,
    )

    return (
        db.query(
            Topic.id.label("topic_id"),
            Topic.name.label("topic_name"),
            total_paper_count.label(
                "paper_count"
            ),
            recent_paper_count.label(
                "recent_paper_count"
            ),
            citation_count.label(
                "citation_count"
            ),
        )
        .join(
            Topic.papers
        )
        .group_by(
            Topic.id,
            Topic.name,
        )
        .order_by(
            desc(recent_paper_count),
            desc(citation_count),
            desc(total_paper_count),
            Topic.id.desc(),
        )
        .limit(limit)
        .all()
    )


# ============================================================
# Count Papers By Topic
# ============================================================

def count_papers_by_topic_id(
    db: Session,
    topic_id: int,
) -> Optional[int]:
    """
    Count papers belonging to a topic.

    Returns None when the topic does not exist.
    """

    topic_exists = (
        db.query(Topic.id)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )

    if topic_exists is None:
        return None

    return (
        db.query(
            func.count(Paper.id)
        )
        .join(
            Paper.topics
        )
        .filter(
            Topic.id == topic_id
        )
        .scalar()
        or 0
    )


# ============================================================
# Find Papers By Topic ID
# ============================================================

def find_papers_by_topic_id(
    db: Session,
    topic_id: int,
    page: int = 1,
    limit: int = 10,
) -> Optional[List[Paper]]:
    """
    Find one page of papers for a topic.

    Pagination is performed by PostgreSQL.
    """

    page = max(
        page,
        1,
    )

    limit = max(
        1,
        min(
            limit,
            20,
        ),
    )

    topic_exists = (
        db.query(Topic.id)
        .filter(
            Topic.id == topic_id
        )
        .first()
    )

    if topic_exists is None:
        return None

    offset = (
        page - 1
    ) * limit

    return (
        db.query(Paper)
        .join(
            Paper.topics
        )
        .filter(
            Topic.id == topic_id
        )
        .order_by(
            Paper.cited_by_count.desc(),
            Paper.publication_year.desc(),
            Paper.id.desc(),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )