from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException
from app.database.database import get_db
from app.schemas.paper_schema import (
    PaginatedPaperResponse,
    PaperCollectionResponse,
    PaperDetailResponse,
)
from app.services.paper_service import (
    search_papers,
    get_paper_by_id,
    get_paper_by_name,
    get_papers_by_ids,
    get_papers_by_names,
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
    summary="Get Papers",
)
def get_papers(
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
            description="Number of papers per page.",
        ),
    ] = settings.DEFAULT_PAGE_SIZE,

    keyword: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_KEYWORD_LENGTH,
            description="Search paper title or abstract.",
        ),
    ] = None,

    year: Annotated[
        Optional[int],
        Query(
            ge=settings.MIN_PUBLICATION_YEAR,
            le=settings.MAX_PUBLICATION_YEAR,
            description="Filter by publication year.",
        ),
    ] = None,

    topic: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_TOPIC_LENGTH,
            description="Filter by topic name.",
        ),
    ] = None,

    author: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_AUTHOR_LENGTH,
            description="Filter by author name.",
        ),
    ] = None,

    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get paginated research papers.

    Supports optional filtering by:
        - keyword
        - publication year
        - topic
        - author
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
# GET /papers/name
# ============================================================
# IMPORTANT:
# This must be registered BEFORE /{paper_id}
# so that "name" is not interpreted as an integer paper_id.
# ============================================================

@router.get(
    "/name",
    response_model=PaperDetailResponse,
    summary="Get Paper By Name",
)
def get_paper_by_name_endpoint(
    name: Annotated[
        str,
        Query(
            min_length=1,
            max_length=1000,
            description="Exact paper title.",
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get a single paper by its name.

    Matching is case-insensitive.
    """

    paper_name = name.strip()

    paper = get_paper_by_name(
        db=db,
        paper_name=paper_name,
    )

    if paper is None:
        raise ResourceNotFoundException(
            resource="Paper",
            resource_id=paper_name,
        )

    return paper


# ============================================================
# GET /papers/collection/ids
# ============================================================

@router.get(
    "/collection/ids",
    response_model=PaperCollectionResponse,
    summary="Get Paper Collection By IDs",
)
def get_paper_collection_by_ids(
    ids: Annotated[
        str,
        Query(
            min_length=1,
            description=(
                "Comma-separated paper IDs. "
                "Example: 101,102,103"
            ),
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get multiple papers by comma-separated paper IDs.

    Duplicate IDs are removed while preserving order.
    """

    paper_ids = _parse_paper_ids(ids)

    return get_papers_by_ids(
        db=db,
        paper_ids=paper_ids,
    )


# ============================================================
# GET /papers/collection/names
# ============================================================

@router.get(
    "/collection/names",
    response_model=PaperCollectionResponse,
    summary="Get Paper Collection By Names",
)
def get_paper_collection_by_names(
    names: Annotated[
        str,
        Query(
            min_length=1,
            max_length=5000,
            description="Comma-separated paper names.",
        ),
    ],
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get multiple papers by comma-separated paper names.

    Duplicate names are removed case-insensitively
    while preserving order.
    """

    paper_names = _parse_paper_names(names)

    return get_papers_by_names(
        db=db,
        paper_names=paper_names,
    )


# ============================================================
# GET /papers/{paper_id}
# ============================================================
# IMPORTANT:
# Keep this AFTER all static routes.
#
# This is necessary for correct routing:
#
# /papers/name
# /papers/collection/ids
# /papers/collection/names
#
# must not be interpreted as:
#
# /papers/{paper_id}
# ============================================================

@router.get(
    "/{paper_id}",
    response_model=PaperDetailResponse,
    summary="Get Paper By ID",
)
def get_paper(
    paper_id: int,
    db: Annotated[
        Session,
        Depends(get_db),
    ] = None,
):
    """
    Get complete paper details by database ID.
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


# ============================================================
# Private Parsing Helpers
# ============================================================

def _parse_paper_ids(
    value: str,
) -> list[int]:
    """
    Parse comma-separated paper IDs.

    Duplicate IDs are removed while preserving order.
    """

    paper_ids: list[int] = []

    for raw_value in value.split(","):
        item = raw_value.strip()

        if not item:
            continue

        if not item.isdigit():
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid paper ID: '{item}'. "
                    "Paper IDs must be positive integers."
                ),
            )

        paper_id = int(item)

        if paper_id <= 0:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid paper ID: '{item}'. "
                    "Paper ID must be greater than zero."
                ),
            )

        paper_ids.append(paper_id)

    if not paper_ids:
        raise HTTPException(
            status_code=400,
            detail="At least one valid paper ID is required.",
        )

    return list(dict.fromkeys(paper_ids))


def _parse_paper_names(
    value: str,
) -> list[str]:
    """
    Parse comma-separated paper names.

    Duplicate names are removed case-insensitively
    while preserving order.
    """

    paper_names: list[str] = []
    seen: set[str] = set()

    for raw_value in value.split(","):
        name = raw_value.strip()

        if not name:
            continue

        normalized = name.casefold()

        if normalized in seen:
            continue

        seen.add(normalized)
        paper_names.append(name)

    if not paper_names:
        raise HTTPException(
            status_code=400,
            detail="At least one paper name is required.",
        )

    return paper_names