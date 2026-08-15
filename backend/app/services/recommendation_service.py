from math import ceil
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper

from app.schemas.recommendation_schema import (
    RecommendationAuthorResponse,
    RecommendationPaperResponse,
    RecommendationTopicResponse,
    TrendingPaperResponse,
)

from app.database.queries.recommendation_queries import (
    count_papers_by_topic_id,
    find_papers_by_topic_id,
    find_similar_papers,
    find_trending_papers,
    get_paper_by_id,
)


# ============================================================
# Constants
# ============================================================

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 20

DEFAULT_RECOMMENDATION_LIMIT = 10
MAX_RECOMMENDATION_LIMIT = 20


class RecommendationService:

    # ========================================================
    # Get Paper
    # ========================================================

    @staticmethod
    def get_paper(
        db: Session,
        paper_id: int,
    ) -> Optional[Paper]:

        return get_paper_by_id(
            db=db,
            paper_id=paper_id,
        )

    # ========================================================
    # Author Mapping
    # ========================================================

    @staticmethod
    def map_author(
        author,
    ) -> RecommendationAuthorResponse:

        return RecommendationAuthorResponse(
            author_id=author.id,
            author_name=author.name,
        )

    # ========================================================
    # Topic Mapping
    # ========================================================

    @staticmethod
    def map_topic(
        topic,
    ) -> RecommendationTopicResponse:

        return RecommendationTopicResponse(
            topic_id=topic.id,
            topic_name=topic.name,
        )

    # ========================================================
    # Paper Mapping
    # ========================================================

    @classmethod
    def map_paper(
        cls,
        paper: Paper,
    ) -> RecommendationPaperResponse:

        return RecommendationPaperResponse(
            paper_id=paper.id,
            paper_name=paper.title,
            abstract=paper.abstract,
            publication_year=paper.publication_year,
            publication_date=(
                paper.publication_date.isoformat()
                if paper.publication_date
                else None
            ),
            doi=paper.doi,
            cited_by_count=paper.cited_by_count,
            authors=[
                cls.map_author(author)
                for author in paper.authors
            ],
            topics=[
                cls.map_topic(topic)
                for topic in paper.topics
            ],
        )

    # ========================================================
    # Multiple Papers Mapping
    # ========================================================

    @classmethod
    def map_papers(
        cls,
        papers: List[Paper],
    ) -> List[RecommendationPaperResponse]:

        return [
            cls.map_paper(paper)
            for paper in papers
        ]

    # ========================================================
    # Trending Mapping
    # ========================================================

    @staticmethod
    def map_trending_paper(
        paper: Paper,
    ) -> TrendingPaperResponse:

        return TrendingPaperResponse(
            paper_id=paper.id,
            paper_name=paper.title,
            publication_year=paper.publication_year,
            cited_by_count=paper.cited_by_count,
        )

    @classmethod
    def map_trending_papers(
        cls,
        papers: List[Paper],
    ) -> List[TrendingPaperResponse]:

        return [
            cls.map_trending_paper(paper)
            for paper in papers
        ]

    # ========================================================
    # Similar Papers
    # ========================================================

    def get_similar(
        self,
        db: Session,
        paper_id: int,
        limit: int,
    ) -> Optional[List[RecommendationPaperResponse]]:

        paper = self.get_paper(
            db=db,
            paper_id=paper_id,
        )

        if paper is None:
            return None

        if paper.embedding is None:
            return []

        limit = max(
            1,
            min(
                limit,
                MAX_RECOMMENDATION_LIMIT,
            ),
        )

        papers = find_similar_papers(
            db=db,
            paper=paper,
            limit=limit,
        )

        return self.map_papers(papers)

    # ========================================================
    # Count Topic Papers
    # ========================================================

    def get_topic_paper_count(
        self,
        db: Session,
        topic_id: int,
    ) -> Optional[int]:

        return count_papers_by_topic_id(
            db=db,
            topic_id=topic_id,
        )

    # ========================================================
    # Paginated Topic Papers
    # ========================================================

    def get_by_topic(
        self,
        db: Session,
        topic_id: int,
        page: int = DEFAULT_PAGE,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Optional[dict]:

        page = max(
            page,
            DEFAULT_PAGE,
        )

        page_size = max(
            1,
            min(
                page_size,
                MAX_PAGE_SIZE,
            ),
        )

        total = self.get_topic_paper_count(
            db=db,
            topic_id=topic_id,
        )

        if total is None:
            return None

        total_pages = (
            ceil(total / page_size)
            if total > 0
            else 0
        )

        papers = find_papers_by_topic_id(
            db=db,
            topic_id=topic_id,
            page=page,
            limit=page_size,
        )

        if papers is None:
            return None

        return {
            "page": page,
            "limit": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages,
            "results": self.map_papers(
                papers
            ),
        }

    # ========================================================
    # Trending
    # ========================================================

    def get_trending(
        self,
        db: Session,
        limit: int = DEFAULT_RECOMMENDATION_LIMIT,
    ) -> List[TrendingPaperResponse]:

        # Trending Research is intentionally limited
        # to the Top 10 by default.

        limit = max(
            1,
            min(
                limit,
                MAX_RECOMMENDATION_LIMIT,
            ),
        )

        papers = find_trending_papers(
            db=db,
            limit=limit,
        )

        return self.map_trending_papers(
            papers
        )


# ============================================================
# Singleton
# ============================================================

recommendation_service = RecommendationService()