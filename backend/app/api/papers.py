from typing import Optional

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

    page: int = Query(
        default=settings.DEFAULT_PAGE,
        ge=1,
        description="Page number",
    ),

    size: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of papers per page",
    ),

    keyword: Optional[str] = Query(
        default=None,
        max_length=settings.MAX_KEYWORD_LENGTH,
        description="Search title or abstract",
    ),

    year: Optional[int] = Query(
        default=None,
        ge=settings.MIN_PUBLICATION_YEAR,
        le=settings.MAX_PUBLICATION_YEAR,
        description="Publication year",
    ),

    topic: Optional[str] = Query(
        default=None,
        max_length=settings.MAX_TOPIC_LENGTH,
        description="Filter by topic",
    ),

    author: Optional[str] = Query(
        default=None,
        max_length=settings.MAX_AUTHOR_LENGTH,
        description="Filter by author",
    ),

    db: Session = Depends(get_db),
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
    db: Session = Depends(get_db),
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