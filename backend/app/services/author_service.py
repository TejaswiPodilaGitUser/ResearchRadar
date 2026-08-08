from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.author import Author


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
        - Pagination
        - Author name search
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

    query = db.query(Author)

    # --------------------------------------------------------
    # Name search
    # --------------------------------------------------------

    if keyword:

        keyword = keyword.strip()

        if keyword:
            query = query.filter(
                Author.name.ilike(
                    f"%{keyword}%"
                )
            )

    # --------------------------------------------------------
    # Count
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(Author.id)
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (
        page - 1
    ) * size

    authors = (
        query
        .order_by(
            Author.name.asc(),
            Author.id.asc(),
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": authors,
    }


# ============================================================
# Get Author
# ============================================================

def get_author_by_id(
    db: Session,
    author_id: int,
) -> Optional[Author]:
    """
    Get author including associated papers.
    """

    return (
        db.query(Author)
        .filter(
            Author.id == author_id
        )
        .first()
    )

