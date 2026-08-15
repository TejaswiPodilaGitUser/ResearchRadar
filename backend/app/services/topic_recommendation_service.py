from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper
from app.models.topic import Topic

from app.database.queries.recommendation_queries import (
    find_emerging_topics,
)

from app.database.queries.topic_recommendation_queries import (
    find_papers_by_same_topics,
)

from app.services.recommendation_service import (
    recommendation_service,
)


DEFAULT_LIMIT = 10
MAX_LIMIT = 20


class TopicRecommendationService:

    # ========================================================
    # Get Topic
    # ========================================================

    @staticmethod
    def get_topic(
        db: Session,
        topic_id: int,
    ) -> Optional[Topic]:

        return (
            db.query(Topic)
            .filter(
                Topic.id == topic_id
            )
            .first()
        )

    # ========================================================
    # By Topic ID
    # ========================================================

    def get_by_topic_id(
        self,
        db: Session,
        topic_id: int,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[List]:

        topic = self.get_topic(
            db=db,
            topic_id=topic_id,
        )

        if topic is None:
            return None

        limit = max(
            1,
            min(
                limit,
                MAX_LIMIT,
            ),
        )

        papers = (
            db.query(Paper)
            .join(
                Paper.topics
            )
            .filter(
                Topic.id == topic_id
            )
            .order_by(
                Paper.cited_by_count.desc(),
                Paper.publication_year.desc(),
                Paper.id.desc(),
            )
            .limit(limit)
            .all()
        )

        return recommendation_service.map_papers(
            papers
        )

    # ========================================================
    # By Paper Topics
    # ========================================================

    def get_by_topic(
        self,
        db: Session,
        paper_id: int,
        limit: int,
    ) -> Optional[List]:

        source_paper = (
            db.query(Paper)
            .filter(
                Paper.id == paper_id
            )
            .first()
        )

        if source_paper is None:
            return None

        topic_ids = [
            topic.id
            for topic in source_paper.topics
        ]

        if not topic_ids:
            return []

        recommendations = find_papers_by_same_topics(
            db=db,
            paper_id=paper_id,
            topic_ids=topic_ids,
            limit=limit,
        )

        return recommendation_service.map_papers(
            recommendations
        )

    # ========================================================
    # Emerging Topics
    # ========================================================

    def get_emerging_topics(
        self,
        db: Session,
        limit: int = DEFAULT_LIMIT,
    ) -> List[dict]:

        # Always return Top 10 by default.

        limit = max(
            1,
            min(
                limit,
                MAX_LIMIT,
            ),
        )

        topics = find_emerging_topics(
            db=db,
            limit=limit,
        )

        return [
            {
                "topic_id": topic.topic_id,
                "topic_name": topic.topic_name,
                "paper_count": topic.paper_count,
                "recent_paper_count": topic.recent_paper_count,
                "citation_count": topic.citation_count,
            }
            for topic in topics
        ]


# ============================================================
# Singleton
# ============================================================

topic_recommendation_service = (
    TopicRecommendationService()
)