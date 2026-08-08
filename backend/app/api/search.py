from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import BadRequestException

from app.database.database import get_db

from app.schemas.paper_schema import (
    PaperListResponse,
)

from app.services.search_service import (
    search_service,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


# ============================================================
# Semantic Search
# ============================================================

@router.get(
    "",
    response_model=List[PaperListResponse],
)
def search_papers(
    q: str = Query(
        ...,
        min_length=settings.MIN_SEARCH_QUERY_LENGTH,
        max_length=settings.MAX_SEARCH_QUERY_LENGTH,
        description="Natural language search query",
    ),

    limit: int = Query(
        default=settings.DEFAULT_SEARCH_LIMIT,
        ge=1,
        le=settings.MAX_SEARCH_RESULTS,
        description="Maximum number of results",
    ),

    db: Session = Depends(get_db),
):
    """
    Perform semantic search across research papers.
    """

    query = q.strip()

    if not query:
        raise BadRequestException(
            message="Search query cannot be empty",
            details={
                "field": "q",
                "error_code": "SEARCH_QUERY_EMPTY",
            },
        )

    results = search_service.search(
        db=db,
        query=query,
        limit=limit,
    )

    return results


# ============================================================
# Hybrid Search
# ============================================================

@router.get(
    "/hybrid",
    response_model=List[PaperListResponse],
)
def hybrid_search_papers(
    q: str = Query(
        ...,
        min_length=settings.MIN_SEARCH_QUERY_LENGTH,
        max_length=settings.MAX_SEARCH_QUERY_LENGTH,
        description="Natural language search query",
    ),

    limit: int = Query(
        default=settings.DEFAULT_SEARCH_LIMIT,
        ge=1,
        le=settings.MAX_SEARCH_RESULTS,
        description="Maximum number of results",
    ),

    db: Session = Depends(get_db),
):
    """
    Perform hybrid search using:

        - Keyword matching
        - Semantic vector similarity
    """

    query = q.strip()

    if not query:
        raise BadRequestException(
            message="Search query cannot be empty",
            details={
                "field": "q",
                "error_code": "SEARCH_QUERY_EMPTY",
            },
        )

    results = search_service.hybrid_search(
        db=db,
        query=query,
        limit=limit,
    )

    return results

