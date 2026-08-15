from typing import List, Optional

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.author import Author


# ============================================================
# Search Authors
# ============================================================

def find_authors(
    db: Session,
    offset: int,
    limit: int,
    keyword: Optional[str] = None,
):
    """
    Find authors using pagination and optional
    name / author ID search.

    Supports:
      - Single name
      - Multiple comma-separated names
      - Single author ID
      - Multiple comma-separated author IDs
      - Mixed IDs and names
    """

    query = db.query(Author)

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        keyword = keyword.strip()

        if keyword:

            search_values = [
                value.strip()
                for value in keyword.split(",")
                if value.strip()
            ]

            conditions = []

            for value in search_values:

                # ------------------------------------------------
                # Author ID
                # ------------------------------------------------

                if value.isdigit():

                    conditions.append(
                        Author.id == int(value)
                    )

                # ------------------------------------------------
                # Author Name
                # ------------------------------------------------

                else:

                    conditions.append(
                        Author.name.ilike(
                            f"%{value}%"
                        )
                    )

            # ------------------------------------------------
            # Combine multiple search values with OR
            # ------------------------------------------------

            if conditions:
                query = query.filter(
                    or_(*conditions)
                )

    # --------------------------------------------------------
    # Total
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(Author.id)
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    authors = (
        query
        .order_by(
            Author.name.asc(),
            Author.id.asc(),
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, authors


# ============================================================
# Get Author By ID
# ============================================================

def find_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[Author]:
    """
    Find an author by database author ID.
    """

    return (
        db.query(Author)
        .filter(
            Author.id == author_id
        )
        .first()
    )


# ============================================================
# Get Author By Name
# ============================================================

def find_author_by_name(
    db: Session,
    author_name: str,
) -> Optional[Author]:
    """
    Find a single author by exact name.

    Matching is case-insensitive.

    Leading and trailing spaces are ignored.

    Examples:
      A Ford
      A. H. Alamoodi
      裕二 池谷
      O'Connor
      Smith-Jones
    """

    if not author_name:
        return None

    normalized_name = author_name.strip()

    if not normalized_name:
        return None

    # --------------------------------------------------------
    # Case-insensitive exact matching
    # --------------------------------------------------------

    return (
        db.query(Author)
        .filter(
            func.lower(
                Author.name
            ) == normalized_name.casefold()
        )
        .first()
    )


# ============================================================
# Get Multiple Authors By IDs
# ============================================================

def find_authors_by_ids(
    db: Session,
    author_ids: List[int],
) -> List[Author]:
    """
    Find multiple authors by their database IDs.

    Duplicate IDs are removed while preserving
    requested order.
    """

    if not author_ids:
        return []

    # --------------------------------------------------------
    # Remove duplicates while preserving order
    # --------------------------------------------------------

    unique_ids = list(
        dict.fromkeys(author_ids)
    )

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    authors = (
        db.query(Author)
        .filter(
            Author.id.in_(unique_ids)
        )
        .all()
    )

    # --------------------------------------------------------
    # Create lookup
    # --------------------------------------------------------

    authors_by_id = {
        author.id: author
        for author in authors
    }

    # --------------------------------------------------------
    # Preserve requested order
    # --------------------------------------------------------

    return [
        authors_by_id[author_id]
        for author_id in unique_ids
        if author_id in authors_by_id
    ]


# ============================================================
# Get Multiple Authors By Names
# ============================================================

def find_authors_by_names(
    db: Session,
    names: List[str],
) -> List[Author]:
    """
    Find multiple authors by exact names.

    Matching is case-insensitive.

    Supports:
      - Spaces
      - Dots
      - Apostrophes
      - Hyphens
      - Unicode characters
    """

    if not names:
        return []

    # --------------------------------------------------------
    # Clean names
    # --------------------------------------------------------

    normalized_names = [
        name.strip()
        for name in names
        if name and name.strip()
    ]

    if not normalized_names:
        return []

    # --------------------------------------------------------
    # Case-insensitive lookup
    # --------------------------------------------------------

    normalized_lookup = [
        name.casefold()
        for name in normalized_names
    ]

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    authors = (
        db.query(Author)
        .filter(
            func.lower(
                Author.name
            ).in_(normalized_lookup)
        )
        .all()
    )

    # --------------------------------------------------------
    # Preserve requested order
    # --------------------------------------------------------

    authors_by_name = {
        author.name.casefold(): author
        for author in authors
        if author.name
    }

    return [
        authors_by_name[name.casefold()]
        for name in normalized_names
        if name.casefold() in authors_by_name
    ]