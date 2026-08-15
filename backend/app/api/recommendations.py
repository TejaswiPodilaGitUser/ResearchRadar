from typing import Annotated, List

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
    EmergingTopicResponse,
    RecommendationListResponse,
    TopicPaperPageResponse,
    TrendingPaperResponse,
)

from app.services.recommendation_service import (
    recommendation_service,
)

from app.services.topic_recommendation_service import (
    topic_recommendation_service,
)


# ============================================================
# Dependencies
# ============================================================

DbSession = Annotated[
    Session,
    Depends(get_db),
]


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


# ============================================================
# Trending Research
# ============================================================

@router.get(
    "/trending",
    response_model=List[TrendingPaperResponse],
)
def get_trending_papers(
    db: DbSession,
    limit: Annotated[
        int,
        Query(
            default=10,
            ge=1,
            le=20,
            description="Number of trending papers",
        ),
    ],
):
    """
    Return Top 10 trending research papers.
    """

    return recommendation_service.get_trending(
        db=db,
        limit=limit,
    )


# ============================================================
# Emerging Topics
# ============================================================

@router.get(
    "/emerging-topics",
    response_model=List[EmergingTopicResponse],
)
def get_emerging_topics(
    db: DbSession,
    limit: Annotated[
        int,
        Query(
            default=10,
            ge=1,
            le=20,
            description="Number of emerging topics",
        ),
    ],
):
    """
    Return Top 10 emerging research topics.
    """

    return topic_recommendation_service.get_emerging_topics(
        db=db,
        limit=limit,
    )


# ============================================================
# Similar Papers
# ============================================================

@router.get(
    "/papers/{paper_id}/similar",
    response_model=RecommendationListResponse,
)
def get_similar_papers(
    paper_id: int,
    db: DbSession,
    limit: Annotated[
        int,
        Query(
            default=10,
            ge=1,
            le=20,
            description="Number of similar papers",
        ),
    ],
):
    """
    Return papers semantically similar to a paper.
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
        "results": result,
    }


# ============================================================
# Topic Similar Papers
# ============================================================

@router.get(
    "/topics/{topic_id}/similar",
    response_model=RecommendationListResponse,
)
def get_similar_papers_by_topic(
    topic_id: int,
    db: DbSession,
    limit: Annotated[
        int,
        Query(
            default=10,
            ge=1,
            le=20,
            description="Number of related papers",
        ),
    ],
):
    """
    Return papers related to a topic.
    """

    result = topic_recommendation_service.get_by_topic_id(
        db=db,
        topic_id=topic_id,
        limit=limit,
    )

    if result is None:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=topic_id,
        )

    return {
        "results": result,
    }


# ============================================================
# Paginated Topic Papers
# ============================================================

@router.get(
    "/topics/{topic_id}/papers",
    response_model=TopicPaperPageResponse,
)
def get_papers_by_topic(
    topic_id: int,
    db: DbSession,
    page: Annotated[
        int,
        Query(
            default=1,
            ge=1,
            description="1-based page number",
        ),
    ],
    limit: Annotated[
        int,
        Query(
            default=10,
            ge=1,
            le=20,
            description="Number of papers per page",
        ),
    ],
):
    """
    Return paginated papers belonging to a topic.

    Example:

        /api/recommendations/topics/123/papers?page=1&limit=10

    Response:

        {
            "topic_id": 123,
            "topic_name": "Natural Language Processing",
            "page": 1,
            "limit": 10,
            "total": 47,
            "total_pages": 5,
            "has_previous": false,
            "has_next": true,
            "results": [...]
        }
    """

    topic = topic_recommendation_service.get_topic(
        db=db,
        topic_id=topic_id,
    )

    if topic is None:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=topic_id,
        )

    pagination = recommendation_service.get_by_topic(
        db=db,
        topic_id=topic_id,
        page=page,
        page_size=limit,
    )

    if pagination is None:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=topic_id,
        )

    return {
        "topic_id": topic.id,
        "topic_name": topic.name,
        **pagination,
    }