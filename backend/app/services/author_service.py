from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException

from app.database.queries.author_queries import (
    find_authors,
    find_author_by_id,
    find_author_by_name,
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
        - Multiple comma-separated IDs/names
    """

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

    total, authors = find_authors(
        db=db,
        offset=offset,
        limit=size,
        keyword=keyword,
    )

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

    if author_id is None or author_id <= 0:
        return None

    author = find_author_by_id(
        db=db,
        author_id=author_id,
    )

    if author is None:
        return None

    papers = [
        _paper_to_response(paper)
        for paper in author.papers
    ]

    return {
        "author_id": author.id,
        "author_name": author.name,
        "orcid": author.orcid,
        "papers": papers,
    }


# ============================================================
# Get Author By Name
# ============================================================

def get_author_by_name(
    db: Session,
    author_name: str,
) -> Optional[dict]:
    """
    Get one author by exact name.

    Matching is case-insensitive.

    Leading and trailing spaces are ignored.
    """

    if not author_name:
        return None

    author_name = author_name.strip()

    if not author_name:
        return None

    author = find_author_by_name(
        db=db,
        author_name=author_name,
    )

    if author is None:
        return None

    papers = [
        _paper_to_response(paper)
        for paper in author.papers
    ]

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

    author_ids = list(
        dict.fromkeys(author_ids)
    )

    if len(author_ids) < 2:
        raise ValueError(
            "At least two author IDs are required."
        )

    authors = find_authors_by_ids(
        db=db,
        author_ids=author_ids,
    )

    authors_by_id = {
        author.id: author
        for author in authors
    }

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

    ordered_authors = [
        authors_by_id[author_id]
        for author_id in author_ids
    ]

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

    Matching is case-insensitive.
    """

    cleaned_names = [
        name.strip()
        for name in author_names
        if name and name.strip()
    ]

    normalized_names = []
    seen_names = set()

    for name in cleaned_names:

        normalized_name = name.casefold()

        if normalized_name in seen_names:
            continue

        seen_names.add(normalized_name)
        normalized_names.append(name)

    author_names = normalized_names

    if len(author_names) < 2:
        raise ValueError(
            "At least two author names are required."
        )

    authors = find_authors_by_names(
        db=db,
        names=author_names,
    )

    authors_by_name = {
        author.name.strip().casefold(): author
        for author in authors
        if author.name
    }

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

    author_ids = [
        authors_by_name[
            name.strip().casefold()
        ].id
        for name in author_names
    ]

    ordered_authors = [
        authors_by_name[
            name.strip().casefold()
        ]
        for name in author_names
    ]

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

    paper_author_ids = {}

    papers_by_id = {}

    for author_id in author_ids:

        author = authors_by_id[
            author_id
        ]

        papers_by_author[
            str(author_id)
        ] = []

        for paper in author.papers:

            papers_by_author[
                str(author_id)
            ].append(
                _paper_to_response(
                    paper
                )
            )

            papers_by_id[
                paper.id
            ] = paper

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

        if len(paper_authors) < 2:
            continue

        paper = papers_by_id[
            paper_id
        ]

        ordered_author_ids = [
            author_id
            for author_id in author_ids
            if author_id in paper_authors
        ]

        shared_papers.append({
            **_paper_to_response(
                paper
            ),
            "author_ids": ordered_author_ids,
            "author_names": [
                authors_by_id[
                    author_id
                ].name
                for author_id in ordered_author_ids
            ],
        })

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    return {
        "authors": author_details,
        "shared_papers": shared_papers,
        "papers_by_author": papers_by_author,
    }