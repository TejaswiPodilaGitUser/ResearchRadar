from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.database import get_db

from app.schemas.author_schema import (
    PaginatedAuthorResponse,
    AuthorDetailResponse,
)

from app.services.author_service import (
    search_authors,
    get_author_by_id,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


# ============================================================
# GET /authors
# ============================================================

@router.get(
    "",
    response_model=PaginatedAuthorResponse,
)
def get_authors(
    page: int = Query(
        default=settings.DEFAULT_PAGE,
        ge=1,
        description="Page number",
    ),

    size: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of authors per page",
    ),

    keyword: Optional[str] = Query(
        default=None,
        max_length=settings.MAX_AUTHOR_LENGTH,
        description="Search authors by name",
    ),

    db: Session = Depends(get_db),
):
    """
    Search and paginate authors.
    """

    return search_authors(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
    )


# ============================================================
# GET /authors/{author_id}
# ============================================================

@router.get(
    "/{author_id}",
    response_model=AuthorDetailResponse,
)
def get_author(
    author_id: int,
    db: Session = Depends(get_db),
):
    """
    Get author details and associated papers.
    """

    author = get_author_by_id(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise HTTPException(
            status_code=404,
            detail=f"Author with id {author_id} not found",
        )

    return author

