from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.queries.paper_queries import (
    find_papers,
    find_paper_by_id,
    find_paper_by_name,
    find_papers_by_ids,
    find_papers_by_names,
)


# ============================================================
# Constants
# ============================================================

DATABASE_SESSION_REQUIRED = (
    "Database session is required."
)


# ============================================================
# Author Mapping
# ============================================================

def _author_to_response(author) -> dict:
    """
    Convert Author model into API response format.
    """

    if author is None:
        return {}

    return {
        "author_id": author.id,
        "author_name": author.name or "",
    }


# ============================================================
# Topic Mapping
# ============================================================

def _topic_to_response(topic) -> dict:
    """
    Convert Topic model into API response format.
    """

    if topic is None:
        return {}

    return {
        "topic_id": topic.id,
        "topic_name": topic.name or "",
    }


# ============================================================
# Paper Mapping
# ============================================================

def _paper_to_response(paper) -> dict:
    """
    Convert Paper model into API response format.

    Used by the paginated paper search endpoint.
    """

    if paper is None:
        return {}

    authors = getattr(
        paper,
        "authors",
        None,
    ) or []

    return {
        "paper_id": paper.id,
        "paper_name": paper.title or "",
        "publication_year": paper.publication_year,
        "cited_by_count": paper.cited_by_count or 0,

        "authors": [
            _author_to_response(author)
            for author in authors
            if author is not None
        ],
    }


# ============================================================
# Paper Detail Mapping
# ============================================================

def _paper_detail_to_response(paper) -> dict:
    """
    Convert Paper model into detailed API response.
    """

    if paper is None:
        return {}

    authors = getattr(
        paper,
        "authors",
        None,
    ) or []

    topics = getattr(
        paper,
        "topics",
        None,
    ) or []

    return {
        "paper_id": paper.id,
        "paper_name": paper.title or "",
        "abstract": paper.abstract,
        "publication_year": paper.publication_year,
        "doi": paper.doi,
        "cited_by_count": paper.cited_by_count or 0,

        "authors": [
            _author_to_response(author)
            for author in authors
            if author is not None
        ],

        "topics": [
            _topic_to_response(topic)
            for topic in topics
            if topic is not None
        ],
    }


# ============================================================
# Search Papers
# ============================================================

def search_papers(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
    year: Optional[int] = None,
    topic: Optional[str] = None,
    author: Optional[str] = None,
):
    """
    Search and filter research papers.

    Business/service layer only.
    """

    if db is None:
        raise ValueError(
            DATABASE_SESSION_REQUIRED
        )

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
        settings.DEFAULT_PAGE,
        page,
    )

    size = max(
        1,
        min(
            size,
            settings.MAX_PAGE_SIZE,
        ),
    )

    offset = (page - 1) * size

    try:
        total, papers = find_papers(
            db=db,
            offset=offset,
            limit=size,
            keyword=keyword,
            year=year,
            topic=topic,
            author=author,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    if papers is None:
        papers = []

    return {
        "page": page,
        "page_size": size,
        "total": total or 0,
        "results": [
            _paper_to_response(paper)
            for paper in papers
            if paper is not None
        ],
    }


# ============================================================
# Get Paper By ID
# ============================================================

def get_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[dict]:
    """
    Get complete paper details by ID.
    """

    if db is None:
        raise ValueError(
            DATABASE_SESSION_REQUIRED
        )

    if paper_id is None or paper_id <= 0:
        return None

    try:
        paper = find_paper_by_id(
            db=db,
            paper_id=paper_id,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    if paper is None:
        return None

    return _paper_detail_to_response(
        paper
    )


# ============================================================
# Get Paper By Name
# ============================================================

def get_paper_by_name(
    db: Session,
    paper_name: str,
) -> Optional[dict]:
    """
    Get complete paper details by paper name.

    Matching is case-insensitive.
    """

    if db is None:
        raise ValueError(
            DATABASE_SESSION_REQUIRED
        )

    if not paper_name or not paper_name.strip():
        return None

    try:
        paper = find_paper_by_name(
            db=db,
            paper_name=paper_name.strip(),
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    if paper is None:
        return None

    return _paper_detail_to_response(
        paper
    )


# ============================================================
# Get Papers By IDs
# ============================================================

def get_papers_by_ids(
    db: Session,
    paper_ids: list[int],
) -> dict:
    """
    Fetch multiple papers by database IDs.

    Characteristics:
        - Removes duplicate IDs.
        - Preserves requested ID order.
        - Performs one collection query.
        - Uses eager relationship loading.
        - Handles missing papers gracefully.
    """

    if db is None:
        raise ValueError(
            DATABASE_SESSION_REQUIRED
        )

    if not paper_ids:
        return {
            "results": [],
            "requested_count": 0,
            "returned_count": 0,
        }

    # --------------------------------------------------------
    # Validate IDs
    # --------------------------------------------------------

    valid_ids: list[int] = []

    for paper_id in paper_ids:
        if paper_id is None:
            continue

        if not isinstance(
            paper_id,
            int,
        ):
            continue

        if paper_id <= 0:
            continue

        valid_ids.append(paper_id)

    # --------------------------------------------------------
    # Remove duplicates while preserving order
    # --------------------------------------------------------

    unique_ids = list(
        dict.fromkeys(valid_ids)
    )

    if not unique_ids:
        return {
            "results": [],
            "requested_count": 0,
            "returned_count": 0,
        }

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    try:
        papers = find_papers_by_ids(
            db=db,
            paper_ids=unique_ids,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    if papers is None:
        papers = []

    # --------------------------------------------------------
    # Map papers by ID
    # --------------------------------------------------------

    papers_by_id = {
        paper.id: paper
        for paper in papers
        if paper is not None
    }

    # --------------------------------------------------------
    # Preserve requested order
    # --------------------------------------------------------

    results = []

    for paper_id in unique_ids:
        paper = papers_by_id.get(
            paper_id
        )

        if paper is None:
            continue

        results.append(
            _paper_detail_to_response(
                paper
            )
        )

    return {
        "results": results,
        "requested_count": len(unique_ids),
        "returned_count": len(results),
    }


# ============================================================
# Get Papers By Names
# ============================================================

def get_papers_by_names(
    db: Session,
    paper_names: list[str],
) -> dict:
    """
    Fetch multiple papers by paper names.

    Characteristics:
        - Case-insensitive matching.
        - Removes duplicate names.
        - Preserves requested order.
        - Performs one collection query.
        - Uses eager relationship loading.
        - Handles missing papers gracefully.
    """

    if db is None:
        raise ValueError(
            DATABASE_SESSION_REQUIRED
        )

    if not paper_names:
        return {
            "results": [],
            "requested_count": 0,
            "returned_count": 0,
        }

    # --------------------------------------------------------
    # Normalize names
    # --------------------------------------------------------

    normalized_names: list[str] = []

    for name in paper_names:
        if not name:
            continue

        normalized_name = name.strip()

        if not normalized_name:
            continue

        normalized_names.append(
            normalized_name
        )

    if not normalized_names:
        return {
            "results": [],
            "requested_count": 0,
            "returned_count": 0,
        }

    # --------------------------------------------------------
    # Remove duplicates case-insensitively
    # --------------------------------------------------------

    unique_names: list[str] = []
    seen_names: set[str] = set()

    for name in normalized_names:
        normalized = name.casefold()

        if normalized in seen_names:
            continue

        seen_names.add(normalized)
        unique_names.append(name)

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    try:
        papers = find_papers_by_names(
            db=db,
            paper_names=unique_names,
        )

    except SQLAlchemyError:
        db.rollback()
        raise

    if papers is None:
        papers = []

    # --------------------------------------------------------
    # Map papers by normalized name
    # --------------------------------------------------------

    papers_by_name = {
        paper.title.casefold(): paper
        for paper in papers
        if paper is not None
        and paper.title
    }

    # --------------------------------------------------------
    # Preserve requested order
    # --------------------------------------------------------

    results = []

    for name in unique_names:
        paper = papers_by_name.get(
            name.casefold()
        )

        if paper is None:
            continue

        results.append(
            _paper_detail_to_response(
                paper
            )
        )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "results": results,
        "requested_count": len(unique_names),
        "returned_count": len(results),
    }