from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.api_metrics import api_metrics
from app.database.database import get_db
from app.models.author import Author
from app.models.paper import Paper
from app.models.topic import Topic


router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"],
)


@router.get("")
def get_metrics(
    db: Annotated[Session, Depends(get_db)],
):
    """
    Return high-level Research Radar corpus metrics.
    """

    total_papers = (
        db.query(func.count(Paper.id)).scalar() or 0
    )

    total_authors = (
        db.query(func.count(Author.id)).scalar() or 0
    )

    total_topics = (
        db.query(func.count(Topic.id)).scalar() or 0
    )

    min_year = (
        db.query(
            func.min(Paper.publication_year)
        ).scalar()
    )

    max_year = (
        db.query(
            func.max(Paper.publication_year)
        ).scalar()
    )

    return {
        "papers": total_papers,
        "authors": total_authors,
        "topics": total_topics,
        "year_range": {
            "from": min_year,
            "to": max_year,
        },
    }


@router.get(
    "/performance",
    summary="Get API performance metrics",
)
def get_api_performance_metrics():
    """
    Return API performance metrics.

    Includes:
    - Total requests
    - Average response time
    - P95 latency
    - Total errors
    - Error rate
    """

    return api_metrics.get_metrics()