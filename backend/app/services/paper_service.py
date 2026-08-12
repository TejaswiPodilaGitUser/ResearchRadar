from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.queries.paper_queries import (
    find_papers,
    find_paper_by_id,
)


# ============================================================
# Paper Mapping
# ============================================================

def _paper_to_response(paper) -> dict:
    """
    Convert Paper model into API response format.
    """

    return {
        "paper_id": paper.id,
        "paper_name": paper.title,
        "publication_year": paper.publication_year,
        "cited_by_count": paper.cited_by_count,
    }


# ============================================================
# Author Mapping
# ============================================================

def _author_to_response(author) -> dict:
    """
    Convert Author model into API response format.
    """

    return {
        "author_id": author.id,
        "author_name": author.name,
    }


# ============================================================
# Topic Mapping
# ============================================================

def _topic_to_response(topic) -> dict:
    """
    Convert Topic model into API response format.
    """

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
    }


# ============================================================
# Paper Detail Mapping
# ============================================================

def _paper_detail_to_response(paper) -> dict:
    """
    Convert Paper model into detailed API response.
    """

    return {
        "paper_id": paper.id,
        "paper_name": paper.title,
        "abstract": paper.abstract,
        "publication_year": paper.publication_year,
        "doi": paper.doi,
        "cited_by_count": paper.cited_by_count,

        "authors": [
            _author_to_response(author)
            for author in paper.authors
        ],

        "topics": [
            _topic_to_response(topic)
            for topic in paper.topics
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

    offset = (
        page - 1
    ) * size

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    total, papers = find_papers(
        db=db,
        offset=offset,
        limit=size,
        keyword=keyword,
        year=year,
        topic=topic,
        author=author,
    )

    # --------------------------------------------------------
    # Response
    # --------------------------------------------------------

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": [
            _paper_to_response(paper)
            for paper in papers
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
    Get complete paper details.
    """

    paper = find_paper_by_id(
        db=db,
        paper_id=paper_id,
    )

    if paper is None:
        return None

    return _paper_detail_to_response(paper)