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
    page: Annotated[int, Query(
        ge=1,
        description="Page number",
    )] = settings.DEFAULT_PAGE,
    size: Annotated[int, Query(
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of papers per page",
    )] = settings.DEFAULT_PAGE_SIZE,
    keyword: Annotated[Optional[str], Query(
        max_length=settings.MAX_KEYWORD_LENGTH,
        description="Search title or abstract",
    )] = None,
    year: Annotated[Optional[int], Query(
        ge=settings.MIN_PUBLICATION_YEAR,
        le=settings.MAX_PUBLICATION_YEAR,
        description="Publication year",
    )] = None,
    topic: Annotated[Optional[str], Query(
        max_length=settings.MAX_TOPIC_LENGTH,
        description="Filter by topic",
    )] = None,
    author: Annotated[Optional[str], Query(
        max_length=settings.MAX_AUTHOR_LENGTH,
        description="Filter by author",
    )] = None,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """
    Search and filter research papers.
    """

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
    db: Annotated[Session, Depends(get_db)] = None,
):
    """
    Get complete paper details.
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