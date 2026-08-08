from typing import Optional

from sqlalchemy import func, or_, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic


# ============================================================
# Search Papers
# ============================================================

def search_papers(
    db: Session,
    page: Optional[int] = None,
    size: Optional[int] = None,
    keyword: Optional[str] = None,
    year: Optional[int] = None,
    topic: Optional[str] = None,
    author: Optional[str] = None,
):
    """
    Search and filter research papers.

    Supports:
        - Pagination
        - Title search
        - Abstract search
        - Publication year
        - Topic
        - Author
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

    offset = (page - 1) * size

    # --------------------------------------------------------
    # Base query
    # --------------------------------------------------------

    query = db.query(Paper)

    # --------------------------------------------------------
    # Keyword filter
    # --------------------------------------------------------

    if keyword:
        keyword = keyword.strip()

        if keyword:
            search_text = f"%{keyword}%"

            query = query.filter(
                or_(
                    Paper.title.ilike(
                        search_text
                    ),
                    Paper.abstract.ilike(
                        search_text
                    ),
                )
            )

    # --------------------------------------------------------
    # Publication year filter
    # --------------------------------------------------------

    if year is not None:
        query = query.filter(
            Paper.publication_year == year
        )

    # --------------------------------------------------------
    # Topic filter
    # --------------------------------------------------------

    if topic:
        topic = topic.strip()

        if topic:
            query = (
                query
                .join(Paper.topics)
                .filter(
                    Topic.name.ilike(
                        f"%{topic}%"
                    )
                )
            )

    # --------------------------------------------------------
    # Author filter
    # --------------------------------------------------------

    if author:
        author = author.strip()

        if author:
            query = (
                query
                .join(Paper.authors)
                .filter(
                    Author.name.ilike(
                        f"%{author}%"
                    )
                )
            )

    # --------------------------------------------------------
    # Total count
    # --------------------------------------------------------

    total = (
        query
        .with_entities(
            func.count(
                func.distinct(Paper.id)
            )
        )
        .scalar()
    ) or 0

    # --------------------------------------------------------
    # Fetch paginated results
    # --------------------------------------------------------

    papers = (
        query
        .distinct()
        .order_by(
            Paper.publication_year.desc(),
            Paper.id.desc(),
        )
        .offset(offset)
        .limit(size)
        .all()
    )

    # --------------------------------------------------------
    # API response
    # --------------------------------------------------------

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "results": papers,
    }


# ============================================================
# Get Paper By ID
# ============================================================

def get_paper_by_id(
    db: Session,
    paper_id: int,
) -> Optional[Paper]:
    """
    Retrieve a paper by database ID.

    Temporary database diagnostics are included here
    to verify that FastAPI is connected to the same
    PostgreSQL database as the ingestion process.
    """

    # --------------------------------------------------------
    # TEMPORARY DATABASE DIAGNOSTICS
    # --------------------------------------------------------

    database = db.execute(
        text("SELECT current_database()")
    ).scalar()

    schema = db.execute(
        text("SELECT current_schema()")
    ).scalar()

    count = db.execute(
        text("SELECT COUNT(*) FROM papers")
    ).scalar()

    paper_exists = db.execute(
        text(
            """
            SELECT id, title
            FROM papers
            WHERE id = :paper_id
            """
        ),
        {
            "paper_id": paper_id,
        },
    ).first()

    print("==========================================")
    print("API DATABASE:", database)
    print("API SCHEMA:", schema)
    print("API PAPER COUNT:", count)
    print("API PAPER ID:", paper_id)
    print("API PAPER EXISTS:", paper_exists)
    print("==========================================")

    # --------------------------------------------------------
    # SQLAlchemy ORM query
    # --------------------------------------------------------

    return (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )

