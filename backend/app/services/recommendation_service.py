from typing import Optional

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.models.author import Author
from app.models.paper import Paper
from app.models.topic import Topic

# IMPORTANT:
# Do NOT import app.models.paper_author.
#
# The project does not have that module.
# The Paper <-> Author relationship is already available
# through Paper.authors / Author.papers.


# ============================================================
# Recommendation Service
# ============================================================


class RecommendationService:
    """
    Central recommendation service.

    Owns:
        - Trending papers
        - Top authors
        - Topics
        - Papers by topic

    Does NOT modify:
        - PaperDetailPage
        - Similar-paper recommendation flow
        - AuthorRecommendationService
        - TopicRecommendationService
        - Existing paper services
    """

    # ========================================================
    # Trending Papers
    # ========================================================

    def get_trending(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Return the top trending papers.

        Ranking:
            1. Citation count DESC
            2. Publication year DESC
            3. Paper ID DESC

        IMPORTANT:
        Return ORM Paper objects here.
        The API schema is responsible for exposing only
        safe fields and excluding embedding.
        """

        limit = max(1, min(limit, 10))

        return (
            db.query(Paper)
            .filter(
                Paper.cited_by_count.isnot(None),
            )
            .order_by(
                desc(Paper.cited_by_count),
                desc(Paper.publication_year),
                desc(Paper.id),
            )
            .limit(limit)
            .all()
        )

    # ========================================================
    # Top Authors
    # ========================================================

    def get_top_authors(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Return the top authors.

        Authors with only one paper are excluded.

        Ranking:
            1. Number of papers DESC
            2. Total citations DESC
            3. Author name ASC

        Uses the existing SQLAlchemy relationship instead of
        importing a non-existent PaperAuthor model.
        """

        limit = max(1, min(limit, 10))

        paper_count = func.count(
            func.distinct(Paper.id)
        )

        citation_count = func.coalesce(
            func.sum(
                func.coalesce(
                    Paper.cited_by_count,
                    0,
                )
            ),
            0,
        )

        results = (
            db.query(
                Author.id.label("author_id"),
                Author.name.label("author_name"),
                paper_count.label("paper_count"),
                citation_count.label("citation_count"),
            )
            .join(
                Author.papers,
            )
            .group_by(
                Author.id,
                Author.name,
            )
            .having(
                paper_count > 1,
            )
            .order_by(
                desc(paper_count),
                desc(citation_count),
                Author.name.asc(),
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "author_id": row.author_id,
                "author_name": row.author_name,
                "paper_count": row.paper_count,
                "citation_count": row.citation_count,
            }
            for row in results
        ]

    # ========================================================
    # Topic
    # ========================================================

    def get_topic(
        self,
        db: Session,
        topic_id: int,
    ) -> Optional[Topic]:
        """
        Return a topic by ID.
        """

        return (
            db.query(Topic)
            .filter(
                Topic.id == topic_id,
            )
            .first()
        )

    # ========================================================
    # Topics
    # ========================================================

    def get_topics(
        self,
        db: Session,
        limit: int = 10,
    ):
        """
        Return topics ordered by the number of associated papers.

        This powers:
            Papers by Topic
        """

        limit = max(1, min(limit, 10))

        paper_count = func.count(
            func.distinct(Paper.id)
        )

        return (
            db.query(
                Topic.id.label("topic_id"),
                Topic.name.label("topic_name"),
                paper_count.label("paper_count"),
            )
            .join(
                Topic.papers,
            )
            .group_by(
                Topic.id,
                Topic.name,
            )
            .order_by(
                desc(paper_count),
                Topic.name.asc(),
            )
            .limit(limit)
            .all()
        )

    # ========================================================
    # Topic Papers
    # ========================================================

    def get_by_topic(
        self,
        db: Session,
        topic_id: int,
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Return paginated papers belonging to a topic.

        Ranking:
            1. Publication year DESC
            2. Citation count DESC
            3. Paper ID DESC

        The query only returns the requested page.
        """

        page = max(1, page)
        page_size = max(1, min(page_size, 10))

        topic = self.get_topic(
            db,
            topic_id,
        )

        if topic is None:
            return None

        base_query = (
            db.query(Paper)
            .join(
                Paper.topics,
            )
            .filter(
                Topic.id == topic_id,
            )
        )

        total = base_query.count()

        total_pages = (
            (total + page_size - 1) // page_size
            if total > 0
            else 0
        )

        offset = (
            page - 1
        ) * page_size

        papers = (
            base_query
            .order_by(
                desc(Paper.publication_year),
                desc(Paper.cited_by_count),
                desc(Paper.id),
            )
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return {
            "topic_id": topic.id,
            "topic_name": topic.name,
            "page": page,
            "limit": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_previous": page > 1,
            "has_next": page < total_pages,
            "results": papers,
        }


# ============================================================
# Singleton
# ============================================================

recommendation_service = RecommendationService()