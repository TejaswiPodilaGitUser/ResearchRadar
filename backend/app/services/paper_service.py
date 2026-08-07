from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.paper import Paper
from app.models.author import Author
from app.models.topic import Topic



def search_papers(
        db: Session,
        page: int = 1,
        size: int = 20,
        keyword: Optional[str] = None,
        year: Optional[int] = None,
        topic: Optional[str] = None,
        author: Optional[str] = None
):

    """
    Search papers with filters

    Supports:
    - pagination
    - title search
    - abstract search
    - year filter
    - topic filter
    - author filter
    """


    query = db.query(Paper)



    # Keyword search
    if keyword:

        search_text = f"%{keyword}%"

        query = query.filter(
            or_(
                Paper.title.ilike(search_text),
                Paper.abstract.ilike(search_text)
            )
        )



    # Year filter
    if year:

        query = query.filter(
            Paper.publication_year == year
        )



    # Topic filter

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



    # Author filter

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



    # Total count before pagination

    total = query.count()



    papers = (
        query
        .offset(
            (page - 1) * size
        )
        .limit(size)
        .all()
    )


    return {
        "page": page,
        "size": size,
        "total": total,
        "results": papers
    }





def get_paper_by_id(
        db: Session,
        paper_id: int
):

    """
    Get complete paper details
    including authors and topics
    """


    return (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )