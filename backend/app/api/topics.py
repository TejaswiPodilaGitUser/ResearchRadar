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

from app.schemas.topic_schema import (
    PaginatedTopicResponse,
    TopicDetailResponse,
)

from app.services.topic_service import (
    search_topics,
    get_topic_by_id,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)


# ============================================================
# GET /topics
# ============================================================

@router.get(
    "",
    response_model=PaginatedTopicResponse,
)
def get_topics(
    page: int = Query(
        default=settings.DEFAULT_PAGE,
        ge=1,
        description="Page number",
    ),

    size: int = Query(
        default=settings.DEFAULT_PAGE_SIZE,
        ge=1,
        le=settings.MAX_PAGE_SIZE,
        description="Number of topics per page",
    ),

    keyword: Optional[str] = Query(
        default=None,
        max_length=settings.MAX_TOPIC_LENGTH,
        description="Search topics by name",
    ),

    db: Session = Depends(get_db),
):
    """
    Search and paginate topics.
    """

    return search_topics(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
    )


# ============================================================
# GET /topics/{topic_id}
# ============================================================

@router.get(
    "/{topic_id}",
    response_model=TopicDetailResponse,
)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    """
    Get topic details and associated papers.
    """

    topic = get_topic_by_id(
        db=db,
        topic_id=topic_id,
    )

    if topic is None:

        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=topic_id,
        )

    return topic