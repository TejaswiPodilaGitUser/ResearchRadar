from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.ai.embedding_service import embedding_service
from app.models.paper import Paper


class SearchService:
    """
    Service responsible for searching research papers.

    Supports:
        1. Semantic vector search using pgvector
        2. Basic hybrid search using keyword + vector similarity
    """

    MIN_QUERY_LENGTH = 2
    DEFAULT_LIMIT = 10
    MAX_LIMIT = 100

    def _validate_query(
        self,
        query: str,
    ) -> str:
        """
        Validate and normalize search query.
        """

        if not query:
            return ""

        query = query.strip()

        if len(query) < self.MIN_QUERY_LENGTH:
            return ""

        return query

    def _normalize_limit(
        self,
        limit: int,
    ) -> int:
        """
        Keep result limit within safe bounds.
        """

        return max(
            1,
            min(
                limit,
                self.MAX_LIMIT,
            ),
        )

    def search(
        self,
        db: Session,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> List[Paper]:
        """
        Perform semantic vector search.

        Flow:

            Query
              ↓
            Embedding
              ↓
            pgvector cosine similarity
              ↓
            PostgreSQL
              ↓
            Ranked papers
        """

        # -----------------------------
        # Validate query
        # -----------------------------

        query = self._validate_query(query)

        if not query:
            return []

        # -----------------------------
        # Normalize limit
        # -----------------------------

        limit = self._normalize_limit(limit)

        # -----------------------------
        # Generate query embedding
        # -----------------------------

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        if not query_embedding:
            return []

        # -----------------------------
        # Calculate cosine distance
        #
        # pgvector:
        # lower distance = more similar
        # -----------------------------

        cosine_distance = (
            Paper.embedding.cosine_distance(
                query_embedding
            )
        )

        # -----------------------------
        # Execute semantic search
        # -----------------------------

        return (
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

    def hybrid_search(
        self,
        db: Session,
        query: str,
        limit: int = DEFAULT_LIMIT,
    ) -> List[Paper]:
        """
        Perform hybrid paper search.

        Combines:

            Keyword matching
                  +
            Semantic vector similarity

        Exact title/abstract matches are prioritized,
        followed by semantic similarity.
        """

        # -----------------------------
        # Validate query
        # -----------------------------

        query = self._validate_query(query)

        if not query:
            return []

        # -----------------------------
        # Normalize limit
        # -----------------------------

        limit = self._normalize_limit(limit)

        # -----------------------------
        # Generate query embedding
        # -----------------------------

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        if not query_embedding:
            return []

        # -----------------------------
        # Vector similarity
        # -----------------------------

        cosine_distance = (
            Paper.embedding.cosine_distance(
                query_embedding
            )
        )

        # -----------------------------
        # Keyword matching
        # -----------------------------

        keyword_match = or_(
            Paper.title.ilike(
                f"%{query}%"
            ),
            Paper.abstract.ilike(
                f"%{query}%"
            ),
        )

        # -----------------------------
        # Execute hybrid search
        #
        # Priority:
        #   1. Keyword match
        #   2. Semantic similarity
        # -----------------------------

        return (
            db.query(Paper)
            .filter(
                Paper.embedding.is_not(None)
            )
            .order_by(
                keyword_match.desc(),
                cosine_distance.asc(),
            )
            .limit(limit)
            .all()
        )


# -----------------------------------------
# Singleton service instance
# -----------------------------------------

search_service = SearchService()
