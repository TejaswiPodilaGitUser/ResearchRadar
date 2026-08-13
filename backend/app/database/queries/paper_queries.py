from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import (
    Session,
    selectinload,
)

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
    Find a single paper by database ID.
    """

    return (
        db.query(Paper)
        .options(
            selectinload(Paper.authors),
            selectinload(Paper.topics),
        )
        .filter(
            Paper.id == paper_id
        )
        .first()
    )


# ============================================================
# Get Papers By IDs
# ============================================================

def find_papers_by_ids(
    db: Session,
    paper_ids: list[int],
) -> list[Paper]:
    """
    Find multiple papers by database IDs.

    Optimized for fetching a collection of papers.

    Characteristics:
        - Single primary Paper query.
        - selectinload for authors.
        - selectinload for topics.
        - No N+1 relationship queries.
        - Duplicate IDs are removed before querying.
        - Results are returned in requested ID order.
    """

    # --------------------------------------------------------
    # Empty collection
    # --------------------------------------------------------

    if not paper_ids:
        return []

    # --------------------------------------------------------
    # Remove duplicates while preserving order
    #
    # Example:
    #
    # [101, 102, 101, 103]
    #
    # becomes:
    #
    # [101, 102, 103]
    # --------------------------------------------------------

    unique_ids = list(
        dict.fromkeys(paper_ids)
    )

    # --------------------------------------------------------
    # Fetch papers
    #
    # SQL equivalent:
    #
    # SELECT ...
    # FROM papers
    # WHERE id IN (...)
    #
    # Relationships are loaded using selectinload.
    # --------------------------------------------------------

    papers = (
        db.query(Paper)
        .options(
            selectinload(Paper.authors),
            selectinload(Paper.topics),
        )
        .filter(
            Paper.id.in_(unique_ids)
        )
        .all()
    )

    # --------------------------------------------------------
    # Preserve requested order
    #
    # Database does not guarantee IN(...) ordering.
    #
    # If frontend sends:
    #
    # [103, 101, 102]
    #
    # response will also be:
    #
    # [103, 101, 102]
    # --------------------------------------------------------

    papers_by_id = {
        paper.id: paper
        for paper in papers
    }

    return [
        papers_by_id[paper_id]
        for paper_id in unique_ids
        if paper_id in papers_by_id
    ]

