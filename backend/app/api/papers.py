from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import (
    ResourceNotFoundException,
)

from app.database.database import get_db

from app.schemas.paper_schema import (
    PaginatedPaperResponse,
    PaperDetailResponse,
)

from app.services.paper_service import (
    search_papers,
    get_paper_by_id,
    get_papers_by_ids,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/papers",
    tags=["Papers"],
)


# ============================================================
# GET /papers
# ============================================================

@router.get(
    "",
    response_model=PaginatedPaperResponse,
)
def get_papers(
    page: Annotated[
        int,
        Query(
            ge=1,
            description="Page number",
        ),
    ] = settings.DEFAULT_PAGE,
    size: Annotated[
        int,
        Query(
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Number of papers per page",
        ),
    ] = settings.DEFAULT_PAGE_SIZE,
    keyword: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_KEYWORD_LENGTH,
            description="Search title or abstract",
        ),
    ] = None,
    year: Annotated[
        Optional[int],
        Query(
            ge=settings.MIN_PUBLICATION_YEAR,
            le=settings.MAX_PUBLICATION_YEAR,
            description="Publication year",
        ),
    ] = None,
    topic: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_TOPIC_LENGTH,
            description="Filter by topic",
        ),
    ] = None,
    author: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_AUTHOR_LENGTH,
            description="Filter by author",
        ),
    ] = None,
    paper_ids: Annotated[
        Optional[str],
        Query(
            description=(
                "Comma-separated paper IDs. "
                "Example: 101,102,103"
            ),
        ),
    ] = None,
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Search, filter, or fetch multiple research papers.

    When paper_ids is supplied, papers are fetched by ID.
    Otherwise, the existing search and filter behavior is used.
    """

    # --------------------------------------------------------
    # Paper Collection
    # --------------------------------------------------------

    if paper_ids:
        ids = []

        for value in paper_ids.split(","):
            value = value.strip()

            if not value:
                continue

            if not value.isdigit():
                continue

            paper_id = int(value)

            if paper_id > 0:
                ids.append(paper_id)

        # Remove duplicates while preserving order.
        ids = list(dict.fromkeys(ids))

        if ids:
            return get_papers_by_ids(
                db=db,
                paper_ids=ids,
                page=page,
                size=size,
            )

    # --------------------------------------------------------
    # Existing Search
    # --------------------------------------------------------

    return search_papers(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
        year=year,
        topic=topic,
        author=author,
    )


# ============================================================
# GET /papers/{paper_id}
# ============================================================

@router.get(
    "/{paper_id}",
    response_model=PaperDetailResponse,
)
def get_paper(
    paper_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get complete paper details by ID.
    """

    paper = get_paper_by_id(
        db=db,
        paper_id=paper_id,
    )

    if paper is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_id,
        )

    return paper
