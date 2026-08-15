from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException
from app.database.database import get_db

from app.schemas.author_schema import (
    PaginatedAuthorResponse,
    AuthorDetailResponse,
    MultipleAuthorsResponse,
)

from app.services.author_service import (
    search_authors,
    get_author_by_id,
    get_author_by_name,
    get_multiple_authors,
    get_multiple_authors_by_names,
)


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/authors",
    tags=["Authors"],
)


# ============================================================
# Dependencies
# ============================================================

DbSession = Annotated[
    Session,
    Depends(get_db),
]


# ============================================================
# GET /authors
# ============================================================

@router.get(
    "",
    response_model=PaginatedAuthorResponse,
    summary="Get Author",
)
def get_authors(
    db: DbSession,

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
            description="Number of authors per page",
        ),
    ] = settings.DEFAULT_PAGE_SIZE,

    keyword: Annotated[
        Optional[str],
        Query(
            max_length=settings.MAX_AUTHOR_LENGTH,
            description=(
                "Single author ID or single author name."
            ),
        ),
    ] = None,
):
    """
    Search authors with pagination.

    Supported:

        Single author ID:
        /api/authors?keyword=2150

        Single author name:
        /api/authors?keyword=A%20Ford
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
    summary="Get Author by id",
)
def get_author(
    db: DbSession,
    author_id: int,
):
    """
    Get author details and associated papers.
    """

    author = get_author_by_id(
        db=db,
        author_id=author_id,
    )

    if author is None:
        raise ResourceNotFoundException(
            resource="Author",
            resource_id=author_id,
        )

    return author


# ============================================================
# GET /authors/name
# ============================================================

@router.get(
    "/name",
    response_model=AuthorDetailResponse,
    summary="Get Author By Name",
)
def get_author_by_name_endpoint(
    db: DbSession,

    name: Annotated[
        str,
        Query(
            min_length=1,
            max_length=settings.MAX_AUTHOR_LENGTH,
            description="Exact author name.",
        ),
    ],
):
    """
    Get a single author by name.

    Matching is case-insensitive.

    Leading and trailing spaces are ignored.

    Example:

        /api/authors/name?name=A%20Ford
    """

    author_name = name.strip()

    author = get_author_by_name(
        db=db,
        author_name=author_name,
    )

    if author is None:
        raise ResourceNotFoundException(
            resource="Author",
            resource_id=author_name,
        )

    return author


# ============================================================
# GET /authors/multiple/ids
# ============================================================

@router.get(
    "/multiple/ids",
    response_model=MultipleAuthorsResponse,
    summary="Get Multiple Authors By Ids",
)
def get_multiple_authors_by_ids_endpoint(
    db: DbSession,

    author_ids: Annotated[
        str,
        Query(
            min_length=1,
            description=(
                "Comma-separated author IDs. "
                "Example: 2208,1561,2150"
            ),
        ),
    ],
):
    """
    Get research information for multiple authors
    using author IDs.

    Example:

        /api/authors/multiple/ids?author_ids=2208,1561,2150
    """

    values = [
        value.strip()
        for value in author_ids.split(",")
        if value.strip()
    ]

    if len(values) < 2:
        raise ValueError(
            "At least two author IDs are required."
        )

    if not all(
        value.isdigit()
        for value in values
    ):
        raise ValueError(
            "author_ids must contain only "
            "comma-separated integers."
        )

    parsed_ids = [
        int(value)
        for value in values
    ]

    return get_multiple_authors(
        db=db,
        author_ids=parsed_ids,
    )


# ============================================================
# GET /authors/multiple/names
# ============================================================

@router.get(
    "/multiple/names",
    response_model=MultipleAuthorsResponse,
    summary="Get Multiple Authors By Names",
)
def get_multiple_authors_by_names_endpoint(
    db: DbSession,

    author_names: Annotated[
        str,
        Query(
            min_length=1,
            max_length=settings.MAX_AUTHOR_LENGTH,
            description=(
                "Comma-separated author names. "
                "Example: "
                "A. H. Alamoodi,A Ford,裕二 池谷"
            ),
        ),
    ],
):
    """
    Get research information for multiple authors
    using author names.

    Comma is the only separator.

    Names may contain:

        - spaces
        - dots
        - apostrophes
        - hyphens
        - Unicode characters

    Examples:

        A. H. Alamoodi,A Ford

        裕二 池谷,A. H. Alamoodi

        Μαρία Ανδρέου,A Ford

        O'Connor,Smith-Jones
    """

    names = [
        name.strip()
        for name in author_names.split(",")
        if name.strip()
    ]

    if len(names) < 2:
        raise ValueError(
            "At least two author names are required."
        )

    return get_multiple_authors_by_names(
        db=db,
        author_names=names,
    )