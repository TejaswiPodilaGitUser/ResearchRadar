from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper


# ============================================================
# Get Paper By ID
# ============================================================

def get_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[Paper]:
    """
    Get a paper by its database ID.
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

    Lower cosine distance = higher similarity.
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
    limit: int,
) -> List[Paper]:
    """
    Find trending papers.

    Ranking:
        1. Highest citation count
        2. Most recent publication year
        3. Latest paper ID as tie-breaker

    Only the Paper entity is queried.
    Authors and Topics are not required for
    the trending response.
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