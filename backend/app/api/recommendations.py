from typing import List

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException
from app.database.database import get_db

from app.schemas.recommendation_schema import (
    RecommendationListResponse,
    TrendingPaperResponse,
)

from app.services.recommendation_service import (
    recommendation_service,
)

from app.services.topic_recommendation_service import (
    topic_recommendation_service,
)

from app.services.author_recommendation_service import (
    author_recommendation_service,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


# ============================================================
# GET /api/recommendations/trending
# ============================================================

@router.get(
    "/trending",
    response_model=List[TrendingPaperResponse],
)
def get_trending_papers(
    limit: int = Query(
        default=settings.RECOMMENDATION_DEFAULT_LIMIT,
        ge=1,
        le=settings.RECOMMENDATION_MAX_LIMIT,
        description="Number of trending papers",
    ),
    db: Session = Depends(get_db),
):
    """
    Return trending research papers.

    Ranking:
        1. Citation count
        2. Publication year
        3. Paper ID
    """

    return recommendation_service.get_trending(
        db=db,
        limit=limit,
    )


# ============================================================
# GET /api/recommendations/{paper_id}/similar
# ============================================================

@router.get(
    "/{paper_id}/similar",
    response_model=RecommendationListResponse,
)
def get_similar_papers(
    paper_id: int,
    limit: int = Query(
        default=settings.RECOMMENDATION_DEFAULT_LIMIT,
        ge=1,
        le=settings.RECOMMENDATION_MAX_LIMIT,
    ),
    db: Session = Depends(get_db),
):
    """
    Return semantically similar papers.
    """

    result = recommendation_service.get_similar(
        db=db,
        paper_id=paper_id,
        limit=limit,
    )

    if result is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_id,
        )

    return {
        "results": result
    }


# ============================================================
# GET /api/recommendations/{paper_id}/by-topic
# ============================================================

@router.get(
    "/{paper_id}/by-topic",
    response_model=RecommendationListResponse,
)
def get_topic_recommendations(
    paper_id: int,
    limit: int = Query(
        default=settings.RECOMMENDATION_DEFAULT_LIMIT,
        ge=1,
        le=settings.RECOMMENDATION_MAX_LIMIT,
    ),
    db: Session = Depends(get_db),
):
    """
    Return papers sharing topics with the source paper.
    """

    result = topic_recommendation_service.get_by_topic(
        db=db,
        paper_id=paper_id,
        limit=limit,
    )

    if result is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_id,
        )

    return {
        "results": result
    }


# ============================================================
# GET /api/recommendations/{paper_id}/by-author
# ============================================================

@router.get(
    "/{paper_id}/by-author",
    response_model=RecommendationListResponse,
)
def get_author_recommendations(
    paper_id: int,
    limit: int = Query(
        default=settings.RECOMMENDATION_DEFAULT_LIMIT,
        ge=1,
        le=settings.RECOMMENDATION_MAX_LIMIT,
    ),
    db: Session = Depends(get_db),
):
    """
    Return papers sharing authors with the source paper.
    """

    result = author_recommendation_service.get_by_author(
        db=db,
        paper_id=paper_id,
        limit=limit,
    )

    if result is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_id,
        )

    return {
        "results": result
    }


# ============================================================
# GET /api/recommendations/{paper_id}
# ============================================================

@router.get(
    "/{paper_id}",
    response_model=RecommendationListResponse,
)
def get_recommendations(
    paper_id: int,
    limit: int = Query(
        default=settings.RECOMMENDATION_DEFAULT_LIMIT,
        ge=1,
        le=settings.RECOMMENDATION_MAX_LIMIT,
    ),
    db: Session = Depends(get_db),
):
    """
    Return general recommendations for a paper.
    """

    result = recommendation_service.get_recommendations(
        db=db,
        paper_id=paper_id,
        limit=limit,
    )

    if result is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_id,
        )

    return {
        "results": result
    }