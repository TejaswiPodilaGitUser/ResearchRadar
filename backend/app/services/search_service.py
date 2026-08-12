from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.ai.embedding_service import embedding_service
from app.core.config import settings
from app.models.paper import Paper


class SearchService:
    """
    Service responsible for research paper search.

    Supports:

        1. Semantic search
        2. Hybrid search
    """

    # ========================================================
    # Validate Query
    # ========================================================

    @staticmethod
    def _validate_query(
        query: str,
    ) -> str:
        """
        Clean and validate search query.
        """

        if not query:
            return ""

        query = query.strip()

        if len(query) < settings.MIN_SEARCH_QUERY_LENGTH:
            return ""

        if len(query) > settings.MAX_SEARCH_QUERY_LENGTH:
            return ""

        return query

    # ========================================================
    # Normalize Limit
    # ========================================================

    @staticmethod
    def _normalize_limit(
        limit: int | None,
    ) -> int:
        """
        Keep result limit within configured boundaries.
        """

        if limit is None:
            return settings.DEFAULT_SEARCH_LIMIT

        return max(
            1,
            min(
                limit,
                settings.MAX_SEARCH_RESULTS,
            ),
        )

    # ========================================================
    # Convert Paper
    # ========================================================

    @staticmethod
    def _paper_to_response(
        paper: Paper,
    ) -> dict:
        """
        Convert SQLAlchemy Paper model
        into API response structure.
        """

        return {
            "paper_id": paper.id,
            "paper_name": paper.title,
            "publication_year": paper.publication_year,
            "cited_by_count": paper.cited_by_count,
        }

    # ========================================================
    # Generate Query Embedding
    # ========================================================

    @staticmethod
    def _generate_embedding(
        query: str,
    ):
        """
        Generate embedding for search query.
        """

        embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        if embedding is None:
            return None

        if len(embedding) != settings.EMBEDDING_DIMENSION:
            return None

        return embedding

    # ========================================================
    # Semantic Search
    # ========================================================

    def search(
        self,
        db: Session,
        query: str,
        limit: int | None = None,
    ) -> List[dict]:
        """
        Perform semantic vector search.

        Flow:

            Query
              ↓
            Embedding
              ↓
            pgvector
              ↓
            Cosine similarity
              ↓
            Ranked papers
        """

        # ----------------------------------------------------
        # Validate query
        # ----------------------------------------------------

        query = self._validate_query(query)

        if not query:
            return []

        # ----------------------------------------------------
        # Validate limit
        # ----------------------------------------------------

        limit = self._normalize_limit(limit)

        # ----------------------------------------------------
        # Generate embedding
        # ----------------------------------------------------

        query_embedding = (
            self._generate_embedding(query)
        )

        if query_embedding is None:
            return []

        # ----------------------------------------------------
        # Calculate cosine distance
        # ----------------------------------------------------

        cosine_distance = (
            Paper.embedding.cosine_distance(
                query_embedding
            )
        )

        # ----------------------------------------------------
        # Execute query
        # ----------------------------------------------------

        papers = (
            db.query(Paper)
            .filter(
                Paper.embedding.is_not(None)
            )
            .order_by(
                cosine_distance.asc()
            )
            .limit(limit)
            .all()
        )

        # ----------------------------------------------------
        # Convert response
        # ----------------------------------------------------

        return [
            self._paper_to_response(paper)
            for paper in papers
        ]

    # ========================================================
    # Hybrid Search
    # ========================================================

    def hybrid_search(
        self,
        db: Session,
        query: str,
        limit: int | None = None,
    ) -> List[dict]:
        """
        Perform hybrid search.

        Combines:

            Keyword matching
                    +
            Semantic similarity
        """

        # ----------------------------------------------------
        # Validate query
        # ----------------------------------------------------

        query = self._validate_query(query)

        if not query:
            return []

        # ----------------------------------------------------
        # Validate limit
        # ----------------------------------------------------

        limit = self._normalize_limit(limit)

        # ----------------------------------------------------
        # Generate embedding
        # ----------------------------------------------------

        query_embedding = (
            self._generate_embedding(query)
        )

        if query_embedding is None:
            return []

        # ----------------------------------------------------
        # Vector similarity
        # ----------------------------------------------------

        cosine_distance = (
            Paper.embedding.cosine_distance(
                query_embedding
            )
        )

        # ----------------------------------------------------
        # Keyword matching
        # ----------------------------------------------------

        search_text = f"%{query}%"

        keyword_match = or_(
            Paper.title.ilike(search_text),
            Paper.abstract.ilike(search_text),
        )

        # ----------------------------------------------------
        # Execute hybrid query
        # ----------------------------------------------------

        papers = (
            db.query(Paper)
            .filter(
                Paper.embedding.is_not(None)
            )
            .order_by(
                keyword_match.desc(),
                cosine_distance.asc(),
                Paper.id.desc(),
            )
            .limit(limit)
            .all()
        )

        # ----------------------------------------------------
        # Convert response
        # ----------------------------------------------------

        return [
            self._paper_to_response(paper)
            for paper in papers
        ]


# ============================================================
# Service Instance
# ============================================================

search_service = SearchService()