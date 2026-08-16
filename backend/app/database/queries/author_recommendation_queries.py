from typing import List

from sqlalchemy import func

from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic


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


# ============================================================
# Find Trending Papers
# ============================================================

def find_trending_papers(
    db: Session,
    limit: int = 10,
) -> List[Paper]:
    """
    Find the most trending research papers.

    Ranking:
        1. Citation count
        2. Publication year
        3. Publication date
        4. Paper ID

    Returns Top 10 by default.
    """

    return (
        db.query(Paper)
        .filter(
            Paper.cited_by_count.isnot(None),
        )
        .order_by(
            Paper.cited_by_count.desc(),
            Paper.publication_year.desc(),
            Paper.publication_date.desc(),
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
) -> List[Topic]:
    """
    Find emerging research topics.

    Topics are ranked by:
        1. Number of papers associated with the topic
        2. Number of recent papers
        3. Topic name

    A topic must have at least one associated paper.

    Returns Top 10 by default.
    """

    paper_count = func.count(Paper.id)

    return (
        db.query(Topic)
        .join(Topic.papers)
        .group_by(Topic.id)
        .order_by(
            paper_count.desc(),
            Topic.name.asc(),
        )
        .limit(limit)
        .all()
    )


# ============================================================
# Find Top Authors With Multiple Papers
# ============================================================

def find_top_authors(
    db: Session,
    limit: int = 10,
):
    """
    Find the top authors who have published multiple papers.

    Ranking:
        1. Number of papers
        2. Total citations
        3. Author name

    Only authors with at least two papers are included.

    Returns Top 10 by default.
    """

    paper_count = func.count(Paper.id)
    total_citations = func.coalesce(
        func.sum(Paper.cited_by_count),
        0,
    )

    return (
        db.query(
            Author,
            paper_count.label("paper_count"),
            total_citations.label("total_citations"),
        )
        .join(Author.papers)
        .group_by(Author.id)
        .having(
            paper_count >= 2,
        )
        .order_by(
            paper_count.desc(),
            total_citations.desc(),
            Author.name.asc(),
        )
        .limit(limit)
        .all()
    )