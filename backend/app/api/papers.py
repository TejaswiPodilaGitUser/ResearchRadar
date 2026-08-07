from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.database.database import get_db

from app.services.paper_service import (
    search_papers,
    get_paper_by_id
)

from app.schemas.paper_schema import (
    PaginatedPaperResponse,
    PaperDetailResponse
)


router = APIRouter(
    prefix="/papers",
    tags=["Papers"]
)



@router.get(
    "",
    response_model=PaginatedPaperResponse
)
def get_papers(

    page: int = 1,

    size: int = 20,

    keyword: Optional[str] = None,

    year: Optional[int] = None,

    topic: Optional[str] = None,

    author: Optional[str] = None,


    db: Session = Depends(get_db)

):

    """
    Search papers

    Supports:
    - pagination
    - keyword search
    - year filter
    - topic filter
    - author filter
    """


    return search_papers(
        db=db,
        page=page,
        size=size,
        keyword=keyword,
        year=year,
        topic=topic,
        author=author
    )




@router.get(
    "/{paper_id}",
    response_model=PaperDetailResponse
)
def get_paper(

    paper_id: int,

    db: Session = Depends(get_db)

):

    """
    Get paper details
    """


    paper = get_paper_by_id(
        db,
        paper_id
    )


    if not paper:

        raise HTTPException(
            status_code=404,
            detail="Paper not found"
        )


    return paper