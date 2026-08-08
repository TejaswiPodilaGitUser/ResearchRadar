from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.paper import Paper
from app.schemas.paper_schema import PaperListResponse


router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"],
)


@router.get(
    "/{paper_id}",
    response_model=list[PaperListResponse],
)
def get_recommendations(
    paper_id: int,
    limit: int = Query(
        default=10,
        ge=1,
        le=50,
        description="Number of recommendations",
    ),
    db: Session = Depends(get_db),
):
    """
    Return papers that are semantically similar
    to the requested paper.
    """

    # -----------------------------------------
    # Find source paper
    # -----------------------------------------

    paper = (
        db.query(Paper)
        .filter(
            Paper.id == paper_id
        )
        .first()
    )

    if paper is None:
        raise HTTPException(
            status_code=404,
            detail=f"Paper with id {paper_id} not found",
        )

    if paper.embedding is None:
        return []

    # -----------------------------------------
    # Calculate cosine distance
    # -----------------------------------------

    distance = (
        Paper.embedding.cosine_distance(
            paper.embedding
        )
    )

    # -----------------------------------------
    # Find similar papers
    # -----------------------------------------

    recommendations = (
        db.query(Paper)
        .filter(
            Paper.embedding.is_not(None),
            Paper.id != paper_id,
        )
        .order_by(
            distance.asc()
        )
        .limit(limit)
        .all()
    )

    return recommendations