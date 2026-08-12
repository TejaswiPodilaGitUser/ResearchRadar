from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.queries.author_queries import (
    find_authors,
    find_author_by_id,
)


# ============================================================
# Author Mapping
# ============================================================

def _author_to_response(author) -> dict:
    """
    Convert Author model to API response.
    """

    return {
        "author_id": author.id,
        "author_name": author.name,
        "orcid": author.orcid,
    }


# ============================================================
# Paper Mapping
# ============================================================

def _paper_to_response(paper) -> dict:
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
# Search Authors
# ============================================================

def search_authors(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
):
    """
    Search authors with pagination.
    """

    # --------------------------------------------------------
    # Pagination defaults
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
    # Pagination guardrails
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

    offset = (
        page - 1
    ) * size

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    total, authors = find_authors(
        db=db,
        offset=offset,
        limit=size,
        keyword=keyword,
    )

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": [
            _author_to_response(author)
            for author in authors
        ],
    }


# ============================================================
# Get Author By ID
# ============================================================

def get_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[dict]:
    """
    Get author including associated papers.
    """

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    author = find_author_by_id(
        db=db,
        author_id=author_id,
    )

    if author is None:
        return None

    # --------------------------------------------------------
    # Convert associated papers
    # --------------------------------------------------------

    papers = [
        _paper_to_response(paper)
        for paper in author.papers
    ]

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "author_id": author.id,
        "author_name": author.name,
        "orcid": author.orcid,
        "papers": papers,
    }