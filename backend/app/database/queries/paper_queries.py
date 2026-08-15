from typing import Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, selectinload

from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic


# ============================================================
# Shared Paper Loading Options
# ============================================================

def _paper_query_with_relationships(db: Session):
    """
    Create a Paper query with authors and topics eagerly loaded.
    """

    return (
        db.query(Paper)
        .options(
            selectinload(Paper.authors),
            selectinload(Paper.topics),
        )
    )


# ============================================================
# Exact / Filtered Paper Search
# ============================================================

def find_papers(
    db: Session,
    offset: int,
    limit: int,
    keyword: Optional[str] = None,
    paper_id: Optional[int] = None,
    year: Optional[int] = None,
    topic: Optional[str] = None,
    author: Optional[str] = None,
):
    """
    Search papers using exact paper ID or text/filter criteria.

    Search behavior:

        paper_id
            Exact database ID match.

        keyword
            Partial case-insensitive match against:
                - title
                - abstract

        year
            Exact publication year.

        topic
            Partial case-insensitive topic match.

        author
            Partial case-insensitive author match.

    Returns:
        tuple[int, list[Paper]]
    """

    # Use the shared query so authors and topics are
    # eagerly loaded for all search result types.
    query = _paper_query_with_relationships(db)

    # --------------------------------------------------------
    # Paper ID
    # --------------------------------------------------------

    if paper_id is not None:
        query = query.filter(
            Paper.id == paper_id
        )

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        value = keyword.strip()

        if value:
            search_text = f"%{value}%"

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
        value = topic.strip()

        if value:
            query = (
                query
                .join(Paper.topics)
                .filter(
                    Topic.name.ilike(
                        f"%{value}%"
                    )
                )
            )

    # --------------------------------------------------------
    # Author
    # --------------------------------------------------------

    if author:
        value = author.strip()

        if value:
            query = (
                query
                .join(Paper.authors)
                .filter(
                    Author.name.ilike(
                        f"%{value}%"
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
# Exact Paper By ID
# ============================================================

def find_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[Paper]:
    """
    Find one paper by exact database ID.
    """

    if paper_id is None or paper_id <= 0:
        return None

    return (
        _paper_query_with_relationships(db)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )


# ============================================================
# Exact Paper By Name
# ============================================================

def find_paper_by_name(
    db: Session,
    paper_name: str,
) -> Optional[Paper]:
    """
    Find one paper by exact title.

    Case-insensitive.
    """

    if not paper_name:
        return None

    name = paper_name.strip()

    if not name:
        return None

    return (
        _paper_query_with_relationships(db)
        .filter(
            func.lower(Paper.title)
            == name.casefold()
        )
        .first()
    )


# ============================================================
# Multiple Papers By IDs
# ============================================================

def find_papers_by_ids(
    db: Session,
    paper_ids: list[int],
) -> list[Paper]:
    """
    Find multiple papers by database IDs.

    Missing IDs are ignored.
    Requested order is preserved.
    """

    if not paper_ids:
        return []

    unique_ids = list(
        dict.fromkeys(
            paper_id
            for paper_id in paper_ids
            if isinstance(paper_id, int)
            and paper_id > 0
        )
    )

    if not unique_ids:
        return []

    papers = (
        _paper_query_with_relationships(db)
        .filter(
            Paper.id.in_(unique_ids)
        )
        .all()
    )

    papers_by_id = {
        paper.id: paper
        for paper in papers
        if paper is not None
    }

    return [
        papers_by_id[paper_id]
        for paper_id in unique_ids
        if paper_id in papers_by_id
    ]


# ============================================================
# Multiple Papers By Names
# ============================================================

def find_papers_by_names(
    db: Session,
    paper_names: list[str],
) -> list[Paper]:
    """
    Find multiple papers by exact title.

    Case-insensitive.
    Missing names are ignored.
    Requested order is preserved.
    """

    if not paper_names:
        return []

    unique_names: list[str] = []
    seen_names: set[str] = set()

    for name in paper_names:

        if not name:
            continue

        value = name.strip()

        if not value:
            continue

        normalized = value.casefold()

        if normalized in seen_names:
            continue

        seen_names.add(normalized)
        unique_names.append(value)

    if not unique_names:
        return []

    search_names = [
        name.casefold()
        for name in unique_names
    ]

    papers = (
        _paper_query_with_relationships(db)
        .filter(
            func.lower(Paper.title).in_(
                search_names
            )
        )
        .all()
    )

    papers_by_name = {
        paper.title.casefold(): paper
        for paper in papers
        if paper is not None
        and paper.title
    }

    return [
        papers_by_name[name.casefold()]
        for name in unique_names
        if name.casefold() in papers_by_name
    ]