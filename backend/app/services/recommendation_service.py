from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper

from app.schemas.recommendation_schema import (
    RecommendationPaperResponse,
    RecommendationAuthorResponse,
    RecommendationTopicResponse,
)


class RecommendationService:
    """
    Common recommendation service.

    Responsibilities:
        - Find source paper
        - Semantic similarity
        - Map database models to API responses
    """

    # ========================================================
    # Get Paper
    # ========================================================

    @staticmethod
    def get_paper(
        db: Session,
        paper_id: int,
    ) -> Optional[Paper]:
        """
        Retrieve a paper by database ID.
        """

        return (
            db.query(Paper)
            .filter(
                Paper.id == paper_id
            )
            .first()
        )

    # ========================================================
    # Author Mapping
    # ========================================================

    @staticmethod
    def map_author(author):
        """
        Convert Author model to API response.
        """

        return RecommendationAuthorResponse(
            author_id=author.id,
            author_name=author.name,
        )

    # ========================================================
    # Topic Mapping
    # ========================================================

    @staticmethod
    def map_topic(topic):
        """
        Convert Topic model to API response.
        """

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
        """
        Convert Paper model to recommendation response.
        """

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
        """
        Convert multiple Paper models to API responses.
        """

        return [
            cls.map_paper(paper)
            for paper in papers
        ]

    # ========================================================
    # Semantic Similarity
    # ========================================================

    def get_similar(
        self,
        db: Session,
        paper_id: int,
        limit: int,
    ):
        """
        Find papers semantically similar to source paper.
        """

        paper = self.get_paper(
            db=db,
            paper_id=paper_id,
        )

        if paper is None:
            return None

        if paper.embedding is None:
            return []

        distance = (
            Paper.embedding.cosine_distance(
                paper.embedding
            )
        )

        papers = (
            db.query(Paper)
            .filter(
                Paper.id != paper_id,
                Paper.embedding.is_not(None),
            )
            .order_by(
                distance.asc()
            )
            .limit(limit)
            .all()
        )

        return self.map_papers(papers)

    # ========================================================
    # Trending
    # ========================================================

    def get_trending(
        self,
        db: Session,
        limit: int,
    ):
        """
        Return highly cited and recent papers.
        """

        papers = (
            db.query(Paper)
            .order_by(
                Paper.cited_by_count.desc(),
                Paper.publication_year.desc(),
                Paper.id.desc(),
            )
            .limit(limit)
            .all()
        )

        return self.map_papers(papers)


# ============================================================
# Singleton
# ============================================================

recommendation_service = RecommendationService()