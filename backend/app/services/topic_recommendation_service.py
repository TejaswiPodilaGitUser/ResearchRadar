from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper

from app.database.queries.topic_recommendation_queries import (
    find_papers_by_same_topics,
)

from app.services.recommendation_service import (
    recommendation_service,
)


class TopicRecommendationService:

    # ========================================================
    # By Topic
    # ========================================================

    def get_by_topic(
        self,
        db: Session,
        paper_id: int,
        limit: int,
    ) -> Optional[List[dict]]:
        """
        Return papers that share one or more topics
        with the requested paper.
        """

        # ----------------------------------------------------
        # Find source paper
        # ----------------------------------------------------

        source_paper = (
            db.query(Paper)
            .filter(
                Paper.id == paper_id
            )
            .first()
        )

        if source_paper is None:
            return None

        # ----------------------------------------------------
        # Get source paper topic IDs
        # ----------------------------------------------------

        topic_ids = [
            topic.id
            for topic in source_paper.topics
        ]

        # ----------------------------------------------------
        # No topics
        # ----------------------------------------------------

        if not topic_ids:
            return []

        # ----------------------------------------------------
        # Find papers sharing the topics
        # ----------------------------------------------------

        recommendations = find_papers_by_same_topics(
            db=db,
            paper_id=paper_id,
            topic_ids=topic_ids,
            limit=limit,
        )

        # ----------------------------------------------------
        # Convert models to API response
        # ----------------------------------------------------

        return recommendation_service.map_papers(
            recommendations
        )


# ============================================================
# Singleton
# ============================================================

topic_recommendation_service = TopicRecommendationService()