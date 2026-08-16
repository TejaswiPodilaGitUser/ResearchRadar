from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import (
    case,
    desc,
    func,
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.services.recommendation_service import (
    recommendation_service,
)

from app.services.topic_recommendation_service import (
    topic_recommendation_service,
)

from app.schemas.recommendation_schema import (
    RecommendationAuthor,
    RecommendationPaper,
    RecommendationTopic,
    TopicPapersResponse,
)

from app.models.paper import Paper
from app.models.topic import Topic


# ============================================================
# Router
# ============================================================

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


# ============================================================
# Trending Papers
# ============================================================

@router.get(
    "/trending",
    response_model=List[RecommendationPaper],
)
def get_trending_papers(
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return the top 10 trending papers.
    """

    return recommendation_service.get_trending(
        db=db,
        limit=limit,
    )


# ============================================================
# Emerging Topics
# ============================================================

@router.get(
    "/emerging-topics",
)
def get_emerging_topics(
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return the top emerging topics.

    Emerging topics are ranked using:
        1. Recent paper activity
        2. Citation count
        3. Total paper count
        4. Topic name

    Only aggregated topic information is returned.
    Paper embeddings are never selected.
    """

    # --------------------------------------------------------
    # Find the latest publication year in the corpus
    # --------------------------------------------------------

    latest_year = (
        db.query(
            func.max(
                Paper.publication_year
            )
        )
        .filter(
            Paper.publication_year.isnot(None)
        )
        .scalar()
    )

    if latest_year is None:
        return []

    # --------------------------------------------------------
    # Consider the latest three publication years
    # as recent research activity.
    # --------------------------------------------------------

    recent_year = latest_year - 2

    # --------------------------------------------------------
    # Aggregations
    # --------------------------------------------------------

    paper_count = (
        func.count(
            func.distinct(
                Paper.id
            )
        )
    )

    recent_paper_count = (
        func.count(
            func.distinct(
                case(
                    (
                        Paper.publication_year
                        >= recent_year,
                        Paper.id,
                    ),
                    else_=None,
                )
            )
        )
    )

    citation_count = (
        func.coalesce(
            func.sum(
                func.coalesce(
                    Paper.cited_by_count,
                    0,
                )
            ),
            0,
        )
    )

    # --------------------------------------------------------
    # Optimized aggregation query
    # --------------------------------------------------------

    results = (
        db.query(
            Topic.id.label(
                "topic_id"
            ),
            Topic.name.label(
                "topic_name"
            ),
            paper_count.label(
                "paper_count"
            ),
            recent_paper_count.label(
                "recent_paper_count"
            ),
            citation_count.label(
                "citation_count"
            ),
        )
        .join(
            Topic.papers,
        )
        .group_by(
            Topic.id,
            Topic.name,
        )
        .having(
            paper_count > 0,
        )
        .order_by(
            desc(
                recent_paper_count
            ),
            desc(
                citation_count
            ),
            desc(
                paper_count
            ),
            Topic.name.asc(),
        )
        .limit(limit)
        .all()
    )

    # --------------------------------------------------------
    # Return JSON-safe lightweight objects
    # --------------------------------------------------------

    return [
        {
            "topic_id": int(
                row.topic_id
            ),
            "topic_name": row.topic_name,
            "paper_count": int(
                row.paper_count or 0
            ),
            "recent_paper_count": int(
                row.recent_paper_count or 0
            ),
            "citation_count": int(
                row.citation_count or 0
            ),
        }
        for row in results
    ]


# ============================================================
# Top Authors
# ============================================================

@router.get(
    "/authors",
    response_model=List[RecommendationAuthor],
)
def get_top_authors(
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return the top authors.
    """

    return recommendation_service.get_top_authors(
        db=db,
        limit=limit,
    )


# ============================================================
# Papers By Author
# ============================================================

@router.get(
    "/authors/{author_id}/papers",
)
def get_papers_by_author(
    author_id: int,
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return paginated papers written by the selected author.

    Papers are ordered by:
        1. Publication year
        2. Citation count
        3. Paper ID

    Only lightweight paper fields are returned.
    Embeddings are never returned.
    """

    # --------------------------------------------------------
    # Verify that the author exists
    #
    # Use the existing Paper.authors relationship.
    # No PaperAuthor model import is required.
    # --------------------------------------------------------

    author_exists = (
        db.query(
            Paper.id
        )
        .filter(
            Paper.authors.any(
                id=author_id
            )
        )
        .first()
    )

    if author_exists is None:
        raise HTTPException(
            status_code=404,
            detail="Author not found.",
        )

    # --------------------------------------------------------
    # Get author name
    # --------------------------------------------------------

    author_name = ""

    author_paper = (
        db.query(
            Paper
        )
        .filter(
            Paper.authors.any(
                id=author_id
            )
        )
        .first()
    )

    if author_paper is not None:

        for author in author_paper.authors:

            if author.id == author_id:
                author_name = author.name
                break

    # --------------------------------------------------------
    # Count author's papers
    # --------------------------------------------------------

    total = (
        db.query(
            func.count(
                func.distinct(
                    Paper.id
                )
            )
        )
        .filter(
            Paper.authors.any(
                id=author_id
            )
        )
        .scalar()
        or 0
    )

    # --------------------------------------------------------
    # Pagination
    # --------------------------------------------------------

    offset = (
        page - 1
    ) * limit

    total_pages = (
        (total + limit - 1)
        // limit
        if total > 0
        else 0
    )

    # --------------------------------------------------------
    # Fetch author's papers
    #
    # IMPORTANT:
    # Do NOT select Paper.embedding.
    # --------------------------------------------------------

    papers = (
        db.query(
            Paper.id,
            Paper.title,
            Paper.publication_year,
            Paper.doi,
            Paper.cited_by_count,
        )
        .filter(
            Paper.authors.any(
                id=author_id
            )
        )
        .order_by(
            desc(
                Paper.publication_year
            ),
            desc(
                func.coalesce(
                    Paper.cited_by_count,
                    0,
                )
            ),
            Paper.id.asc(),
        )
        .offset(
            offset
        )
        .limit(
            limit
        )
        .all()
    )

    # --------------------------------------------------------
    # Return paginated response
    #
    # This matches the React
    # AuthorPapersResponse interface.
    # --------------------------------------------------------

    return {
        "author_id": author_id,
        "author_name": author_name,
        "page": page,
        "limit": limit,
        "total": int(total),
        "total_pages": int(total_pages),
        "has_previous": page > 1,
        "has_next": page < total_pages,
        "results": [
            {
                "id": row.id,
                "title": row.title,
                "publication_year": row.publication_year,
                "doi": row.doi,
                "cited_by_count": (
                    row.cited_by_count or 0
                ),
            }
            for row in papers
        ],
    }


# ============================================================
# Topics
# ============================================================

@router.get(
    "/topics",
    response_model=List[RecommendationTopic],
)
def get_topics(
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return topics available for browsing.
    """

    results = recommendation_service.get_topics(
        db=db,
        limit=limit,
    )

    return [
        {
            "topic_id": row.topic_id,
            "topic_name": row.topic_name,
            "paper_count": row.paper_count,
        }
        for row in results
    ]


# ============================================================
# Papers By Topic
# ============================================================

@router.get(
    "/topics/{topic_id}/papers",
    response_model=TopicPapersResponse,
)
def get_papers_by_topic(
    topic_id: int,
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return paginated papers belonging to a topic.
    """

    result = recommendation_service.get_by_topic(
        db=db,
        topic_id=topic_id,
        page=page,
        page_size=limit,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Topic not found.",
        )

    return result


# ============================================================
# Similar Papers
# ============================================================

@router.get(
    "/papers/{paper_id}/similar",
    response_model=List[RecommendationPaper],
)
def get_similar_papers(
    paper_id: int,
    limit: int = Query(
        default=5,
        ge=1,
        le=10,
    ),
    db: Session = Depends(get_db),
):
    """
    Return papers semantically similar to the selected paper.

    The selected paper itself is excluded.

    Similarity is calculated using the stored embedding.
    The embedding is used only for ordering and is never
    included in the API response.
    """

    # --------------------------------------------------------
    # Get source paper embedding
    # --------------------------------------------------------

    source_paper = (
        db.query(
            Paper.id,
            Paper.embedding,
        )
        .filter(
            Paper.id == paper_id,
        )
        .first()
    )

    if source_paper is None:
        raise HTTPException(
            status_code=404,
            detail="Paper not found.",
        )

    if source_paper.embedding is None:
        return []

    # --------------------------------------------------------
    # Calculate cosine similarity
    # --------------------------------------------------------

    similarity_distance = (
        Paper.embedding.cosine_distance(
            source_paper.embedding
        )
    )

    # --------------------------------------------------------
    # Fetch only lightweight paper fields
    # --------------------------------------------------------

    similar_papers = (
        db.query(
            Paper.id,
            Paper.title,
            Paper.publication_year,
            Paper.doi,
            Paper.cited_by_count,
        )
        .filter(
            Paper.id != paper_id,
            Paper.embedding.isnot(None),
        )
        .order_by(
            similarity_distance.asc(),
            Paper.id.asc(),
        )
        .limit(limit)
        .all()
    )

    # --------------------------------------------------------
    # Return plain dictionaries
    #
    # No embedding is returned.
    # --------------------------------------------------------

    return [
        {
            "id": row.id,
            "title": row.title,
            "publication_year": row.publication_year,
            "doi": row.doi,
            "cited_by_count": (
                row.cited_by_count or 0
            ),
        }
        for row in similar_papers
    ]