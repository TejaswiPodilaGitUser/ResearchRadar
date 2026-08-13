from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException

from app.database.queries.author_queries import (
    find_authors,
    find_author_by_id,
    find_authors_by_ids,
    find_authors_by_names,
)


# ============================================================
# Author Mapping
# ============================================================

def _author_to_response(author) -> dict:
    """
    Convert Author model to API response.
    """

    return {
        "author_id": author.id,
        "author_name": author.name,
        "orcid": author.orcid,
    }


# ============================================================
# Paper Mapping
# ============================================================

def _paper_to_response(paper) -> dict:
    """
    Convert Paper model to API response.
    """

    return {
        "paper_id": paper.id,
        "paper_name": paper.title,
        "publication_year": paper.publication_year,
        "cited_by_count": paper.cited_by_count,
    }


# ============================================================
# Search Authors
# ============================================================

def search_authors(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
):
    """
    Search authors with pagination.

    Supports:
        - No keyword
        - Single author ID
        - Single author name
    """

    # --------------------------------------------------------
    # Pagination defaults
    # --------------------------------------------------------

    page = (
        page
        if page is not None
        else settings.DEFAULT_PAGE
    )

    size = (
        size
        if size is not None
        else settings.DEFAULT_PAGE_SIZE
    )

    # --------------------------------------------------------
    # Pagination guardrails
    # --------------------------------------------------------

    page = max(
        page,
        settings.DEFAULT_PAGE,
    )

    size = max(
        1,
        min(
            size,
            settings.MAX_PAGE_SIZE,
        ),
    )

    offset = (
        page - 1
    ) * size

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    total, authors = find_authors(
        db=db,
        offset=offset,
        limit=size,
        keyword=keyword,
    )

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": [
            _author_to_response(author)
            for author in authors
        ],
    }


# ============================================================
# Get Author By ID
# ============================================================

def get_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[dict]:
    """
    Get one author including associated papers.
    """

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    author = find_author_by_id(
        db=db,
        author_id=author_id,
    )

    if author is None:
        return None

    # --------------------------------------------------------
    # Convert associated papers
    # --------------------------------------------------------

    papers = [
        _paper_to_response(paper)
        for paper in author.papers
    ]

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "author_id": author.id,
        "author_name": author.name,
        "orcid": author.orcid,
        "papers": papers,
    }


# ============================================================
# Get Multiple Authors By ID
# ============================================================

def get_multiple_authors(
    db: Session,
    author_ids: list[int],
):
    """
    Get research information across multiple authors.

    Supports two or more authors.

    Returns:
        - authors
        - shared_papers
        - papers_by_author
    """

    # --------------------------------------------------------
    # Remove duplicate IDs while preserving order
    # --------------------------------------------------------

    author_ids = list(
        dict.fromkeys(author_ids)
    )

    # --------------------------------------------------------
    # Validate number of authors
    # --------------------------------------------------------

    if len(author_ids) < 2:
        raise ValueError(
            "At least two author IDs are required."
        )

    # --------------------------------------------------------
    # Find authors
    # --------------------------------------------------------

    authors = find_authors_by_ids(
        db=db,
        author_ids=author_ids,
    )

    # --------------------------------------------------------
    # Create lookup
    # --------------------------------------------------------

    authors_by_id = {
        author.id: author
        for author in authors
    }

    # --------------------------------------------------------
    # Validate requested authors
    # --------------------------------------------------------

    missing_author_ids = [
        author_id
        for author_id in author_ids
        if author_id not in authors_by_id
    ]

    if missing_author_ids:
        raise ResourceNotFoundException(
            resource="Author",
            resource_id=", ".join(
                str(author_id)
                for author_id in missing_author_ids
            ),
        )

    # --------------------------------------------------------
    # Reorder authors according to requested IDs
    # --------------------------------------------------------

    ordered_authors = [
        authors_by_id[author_id]
        for author_id in author_ids
    ]

    # --------------------------------------------------------
    # Build response
    # --------------------------------------------------------

    return _build_multiple_author_response(
        author_ids=author_ids,
        authors=ordered_authors,
    )


# ============================================================
# Get Multiple Authors By Name
# ============================================================

def get_multiple_authors_by_names(
    db: Session,
    author_names: list[str],
):
    """
    Get research information across multiple authors
    using exact author names.

    Comma is handled by the API layer as the separator.

    Supported names include:

        A. H. Alamoodi
        A Ford
        裕二 池谷
        Μαρία Ανδρέου
        O'Connor
        Smith-Jones

    Spaces, dots, apostrophes, hyphens and Unicode
    characters are preserved.
    """

    # --------------------------------------------------------
    # Clean names
    # --------------------------------------------------------

    cleaned_names = [
        name.strip()
        for name in author_names
        if name and name.strip()
    ]

    # --------------------------------------------------------
    # Remove duplicate names while preserving order
    # --------------------------------------------------------

    normalized_names = []
    seen_names = set()

    for name in cleaned_names:

        normalized_name = name.casefold()

        if normalized_name in seen_names:
            continue

        seen_names.add(normalized_name)
        normalized_names.append(name)

    author_names = normalized_names

    # --------------------------------------------------------
    # Validate number of authors
    # --------------------------------------------------------

    if len(author_names) < 2:
        raise ValueError(
            "At least two author names are required."
        )

    # --------------------------------------------------------
    # Find authors
    # --------------------------------------------------------

    authors = find_authors_by_names(
        db=db,
        names=author_names,
    )

    # --------------------------------------------------------
    # Create case-insensitive lookup
    # --------------------------------------------------------

    authors_by_name = {
        author.name.strip().casefold(): author
        for author in authors
    }

    # --------------------------------------------------------
    # Validate requested authors exist
    # --------------------------------------------------------

    missing_author_names = [
        name
        for name in author_names
        if name.strip().casefold()
        not in authors_by_name
    ]

    if missing_author_names:
        raise ResourceNotFoundException(
            resource="Author",
            resource_id=", ".join(
                missing_author_names
            ),
        )

    # --------------------------------------------------------
    # Convert names to IDs
    #
    # Preserve requested order.
    # --------------------------------------------------------

    author_ids = [
        authors_by_name[
            name.strip().casefold()
        ].id
        for name in author_names
    ]

    # --------------------------------------------------------
    # Reorder authors according to requested names
    # --------------------------------------------------------

    ordered_authors = [
        authors_by_name[
            name.strip().casefold()
        ]
        for name in author_names
    ]

    # --------------------------------------------------------
    # Build response
    # --------------------------------------------------------

    return _build_multiple_author_response(
        author_ids=author_ids,
        authors=ordered_authors,
    )


# ============================================================
# Build Multiple Author Response
# ============================================================

def _build_multiple_author_response(
    author_ids: list[int],
    authors: list,
):
    """
    Build the common multiple-author response.

    Returns:

        authors
        shared_papers
        papers_by_author
    """

    # --------------------------------------------------------
    # Create author lookup
    # --------------------------------------------------------

    authors_by_id = {
        author.id: author
        for author in authors
    }

    # --------------------------------------------------------
    # Author information
    # --------------------------------------------------------

    author_details = [
        _author_to_response(
            authors_by_id[author_id]
        )
        for author_id in author_ids
    ]

    # --------------------------------------------------------
    # Papers by author
    # --------------------------------------------------------

    papers_by_author = {}

    # paper_id -> selected author IDs
    paper_author_ids = {}

    # paper_id -> paper object
    papers_by_id = {}

    for author_id in author_ids:

        author = authors_by_id[
            author_id
        ]

        papers_by_author[
            str(author_id)
        ] = []

        for paper in author.papers:

            # ------------------------------------------------
            # Add paper under author
            # ------------------------------------------------

            papers_by_author[
                str(author_id)
            ].append(
                _paper_to_response(
                    paper
                )
            )

            # ------------------------------------------------
            # Keep paper object
            # ------------------------------------------------

            papers_by_id[
                paper.id
            ] = paper

            # ------------------------------------------------
            # Track selected authors for paper
            # ------------------------------------------------

            paper_author_ids.setdefault(
                paper.id,
                set(),
            ).add(author_id)

    # --------------------------------------------------------
    # Shared papers
    # --------------------------------------------------------

    shared_papers = []

    for (
        paper_id,
        paper_authors,
    ) in paper_author_ids.items():

        # ----------------------------------------------------
        # Paper must belong to at least two
        # selected authors.
        # ----------------------------------------------------

        if len(paper_authors) < 2:
            continue

        paper = papers_by_id[
            paper_id
        ]

        # ----------------------------------------------------
        # Preserve requested author order
        # ----------------------------------------------------

        ordered_author_ids = [
            author_id
            for author_id in author_ids
            if author_id in paper_authors
        ]

        # ----------------------------------------------------
        # Shared paper response
        # ----------------------------------------------------

        shared_papers.append({
            **_paper_to_response(
                paper
            ),

            "author_ids":
                ordered_author_ids,

            "author_names": [
                authors_by_id[
                    author_id
                ].name
                for author_id
                in ordered_author_ids
            ],
        })

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "authors": author_details,

        "shared_papers":
            shared_papers,

        "papers_by_author":
            papers_by_author,
    }