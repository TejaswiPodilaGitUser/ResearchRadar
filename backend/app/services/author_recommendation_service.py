from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.paper import Paper

from app.database.queries.author_recommendation_queries import (
    find_papers_by_same_authors,
)

from app.services.recommendation_service import (
    recommendation_service,
)


class AuthorRecommendationService:

    # ========================================================
    # By Author
    # ========================================================

    def get_by_author(
        self,
        db: Session,
        paper_id: int,
        limit: int,
    ) -> Optional[List[dict]]:
        """
        Return papers that share one or more authors
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
        # Get source paper author IDs
        # ----------------------------------------------------

        author_ids = [
            author.id
            for author in source_paper.authors
        ]

        # ----------------------------------------------------
        # No authors
        # ----------------------------------------------------

        if not author_ids:
            return []

        # ----------------------------------------------------
        # Find papers sharing authors
        # ----------------------------------------------------

        recommendations = find_papers_by_same_authors(
            db=db,
            paper_id=paper_id,
            author_ids=author_ids,
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

author_recommendation_service = AuthorRecommendationService()