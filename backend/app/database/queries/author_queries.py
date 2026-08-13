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

    Examples:
      2150
      A Ford
      2150,1561,2208
      A Ford,A. H. Alamoodi
      2150,A Ford,1561
      裕二 池谷,A. H. Alamoodi
    """

    query = db.query(Author)

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    if keyword:
        keyword = keyword.strip()

        if keyword:

            # ------------------------------------------------
            # IMPORTANT:
            # Comma is the ONLY author separator.
            #
            # This means:
            #
            # A. H. Alamoodi
            #
            # remains one author name.
            #
            # 裕二 池谷
            #
            # also remains one author name.
            # ------------------------------------------------

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
# Get Author
# ============================================================

def find_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[Author]:
    """
    Find an author by database author_id.
    """

    return (
        db.query(Author)
        .filter(
            Author.id == author_id
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
      - Unicode characters

    Examples:
      A Ford
      A. H. Alamoodi
      裕二 池谷
      O'Connor
    """

    if not names:
        return []

    # --------------------------------------------------------
    # Clean names
    # --------------------------------------------------------

    normalized_names = [
        name.strip()
        for name in names
        if name.strip()
    ]

    if not normalized_names:
        return []

    # --------------------------------------------------------
    # Case-insensitive exact matching
    #
    # casefold() is used instead of lower() for
    # better Unicode handling.
    # --------------------------------------------------------

    normalized_lookup = [
        name.casefold()
        for name in normalized_names
    ]

    # --------------------------------------------------------
    # Database query
    # --------------------------------------------------------

    return (
        db.query(Author)
        .filter(
            func.lower(
                Author.name
            ).in_(
                normalized_lookup
            )
        )
        .all()
    )
