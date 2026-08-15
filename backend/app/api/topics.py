from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
)
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException
from app.database.database import get_db

from app.schemas.topic_schema import (
    PaginatedTopicResponse,
    TopicDetailResponse,
)

from app.services.topic_service import (
    search_topics,
    get_topic_by_id,
    get_topic_by_name,
    get_multiple_topics,
    get_multiple_topics_by_names,
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
    summary="Get Topics",
)
def get_topics(
    page: Annotated[
        int,
        Query(
            ge=1,
            description="Page number.",
        ),
    ] = settings.DEFAULT_PAGE,

    size: Annotated[
        int,
        Query(
            ge=1,
            le=settings.MAX_PAGE_SIZE,
            description="Number of topics per page.",
        ),
    ] = settings.DEFAULT_PAGE_SIZE,

    keyword: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_TOPIC_LENGTH,
            description="Search topic by name or topic ID.",
        ),
    ] = None,

    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get paginated research topics.

    Supports optional filtering by topic name or topic ID.
    """

    return search_topics(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
    )


# ============================================================
# GET /topics/{topic_id}
# IMPORTANT:
# - This endpoint must remain an integer ID route.
# - /topics/name will NOT be treated as topic_id.
# ============================================================

@router.get(
    "/{topic_id:int}",
    response_model=TopicDetailResponse,
    summary="Get Topic By ID",
    responses={
        404: {
            "description": "Topic not found.",
        },
    },
)
def get_topic(
    topic_id: Annotated[
        int,
        Path(
            ge=1,
            description="Topic database ID.",
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get complete topic details by database ID.
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


# ============================================================
# GET /topics/name
# ============================================================

@router.get(
    "/name",
    response_model=TopicDetailResponse,
    summary="Get Topic By Name",
    responses={
        400: {
            "description": "Invalid topic name.",
        },
        404: {
            "description": "Topic not found.",
        },
    },
)
def get_topic_by_name_endpoint(
    name: Annotated[
        str,
        Query(
            min_length=1,
            max_length=settings.MAX_TOPIC_LENGTH,
            description="Exact topic name.",
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get a single topic by exact name.

    Matching is case-insensitive.
    """

    topic_name = name.strip()

    if not topic_name:
        raise HTTPException(
            status_code=400,
            detail="Topic name cannot be empty.",
        )

    topic = get_topic_by_name(
        db=db,
        topic_name=topic_name,
    )

    if topic is None:
        raise ResourceNotFoundException(
            resource="Topic",
            resource_id=topic_name,
        )

    return topic


# ============================================================
# GET /topics/multiple/ids
# ============================================================

@router.get(
    "/multiple/ids",
    response_model=dict,
    summary="Get Multiple Topics By IDs",
    responses={
        400: {
            "description": (
                "Invalid topic IDs or fewer than two "
                "topic IDs provided."
            ),
        },
        404: {
            "description": "One or more topics not found.",
        },
    },
)
def get_multiple_topics_by_ids(
    ids: Annotated[
        str,
        Query(
            min_length=1,
            description=(
                "Comma-separated topic IDs. "
                "Example: 1,2,3"
            ),
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get research information across multiple topics
    using comma-separated topic IDs.

    At least two topic IDs are required.
    Duplicate IDs are removed while preserving order.
    """

    topic_ids = _parse_topic_ids(ids)

    if len(topic_ids) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two topic IDs are required.",
        )

    return get_multiple_topics(
        db=db,
        topic_ids=topic_ids,
    )


# ============================================================
# GET /topics/multiple/names
# ============================================================

@router.get(
    "/multiple/names",
    response_model=dict,
    summary="Get Multiple Topics By Names",
    responses={
        400: {
            "description": (
                "Invalid topic names or fewer than two "
                "topic names provided."
            ),
        },
        404: {
            "description": "One or more topics not found.",
        },
    },
)
def get_multiple_topics_by_names_endpoint(
    names: Annotated[
        str,
        Query(
            min_length=1,
            max_length=5000,
            description="Comma-separated topic names.",
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get research information across multiple topics
    using comma-separated topic names.

    At least two topic names are required.
    Duplicate names are removed case-insensitively
    while preserving order.
    """

    topic_names = _parse_topic_names(names)

    if len(topic_names) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two topic names are required.",
        )

    return get_multiple_topics_by_names(
        db=db,
        topic_names=topic_names,
    )


# ============================================================
# Private Parsing Helpers
# ============================================================

def _parse_topic_ids(
    value: str,
) -> list[int]:
    """
    Parse comma-separated topic IDs.

    Guardrails:
        - Empty values are ignored.
        - IDs must be positive integers.
        - Duplicate IDs are removed.
        - Original order is preserved.
    """

    topic_ids: list[int] = []

    for raw_value in value.split(","):
        item = raw_value.strip()

        if not item:
            continue

        if not item.isdigit():
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid topic ID: '{item}'. "
                    "Topic IDs must be positive integers."
                ),
            )

        topic_id = int(item)

        if topic_id <= 0:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid topic ID: '{item}'. "
                    "Topic ID must be greater than zero."
                ),
            )

        topic_ids.append(topic_id)

    if not topic_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one valid topic ID is required.",
        )

    return list(dict.fromkeys(topic_ids))


def _parse_topic_names(
    value: str,
) -> list[str]:
    """
    Parse comma-separated topic names.

    Guardrails:
        - Empty names are ignored.
        - Names are trimmed.
        - Duplicate names are removed case-insensitively.
        - Original order is preserved.
    """

    topic_names: list[str] = []
    seen: set[str] = set()

    for raw_value in value.split(","):
        name = raw_value.strip()

        if not name:
            continue

        normalized = name.casefold()

        if normalized in seen:
            continue

        seen.add(normalized)
        topic_names.append(name)

    if not topic_names:
        raise HTTPException(
            status_code=400,
            detail="At least one topic name is required.",
        )

    return topic_names