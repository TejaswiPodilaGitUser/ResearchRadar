from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.queries.paper_queries import (
    find_papers,
    find_paper_by_id,
    find_papers_by_ids,
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

    offset = (
        page - 1
    ) * size

    total, papers = find_papers(
        db=db,
        offset=offset,
        limit=size,
        keyword=keyword,
        year=year,
        topic=topic,
        author=author,
    )

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


# ============================================================
# Get Paper Collection
# ============================================================

def get_paper_collection(
    db: Session,
    paper_ids: list[int],
) -> dict:
    """
    Fetch multiple papers by their IDs.

    This operation is read-only. POST is used at the API
    layer so a potentially large collection of IDs does not
    need to be exposed in the URL.
    """

    # --------------------------------------------------------
    # Remove duplicates while preserving requested order
    # --------------------------------------------------------

    unique_ids = list(
        dict.fromkeys(paper_ids)
    )

    if not unique_ids:
        return {
            "count": 0,
            "requested_count": 0,
            "results": [],
        }

    # --------------------------------------------------------
    # Fetch papers
    # --------------------------------------------------------

    papers = find_papers_by_ids(
        db=db,
        paper_ids=unique_ids,
    )

    # --------------------------------------------------------
    # Map database results by ID
    # --------------------------------------------------------

    papers_by_id = {
        paper.id: paper
        for paper in papers
    }

    # --------------------------------------------------------
    # Preserve requested ID order
    # --------------------------------------------------------

    results = []

    for paper_id in unique_ids:
        paper = papers_by_id.get(paper_id)

        if paper is not None:
            results.append(
                _paper_detail_to_response(
                    paper
                )
            )

    return {
        "count": len(results),
        "requested_count": len(unique_ids),
        "results": results,
    }

# ============================================================
# Get Paper Collection
# ============================================================

def get_papers_by_ids(
    db: Session,
    paper_ids: list[int],
) -> list[dict]:
    """
    Fetch multiple papers by their database IDs.

    Read-only operation.
    """

    if not paper_ids:
        return []

    papers = find_papers_by_ids(
        db=db,
        paper_ids=paper_ids,
    )

    return [
        _paper_detail_to_response(paper)
        for paper in papers
    ]