from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# Paper Recommendation
# ============================================================


class RecommendationPaper(BaseModel):
    """
    Safe paper representation for recommendation APIs.

    Used by:
        - Trending papers
        - Topic papers

    embedding is intentionally NOT included.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    title: str
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    cited_by_count: int = 0


# ============================================================
# Similar Paper
# ============================================================


class SimilarPaper(BaseModel):
    """
    Paper representation used only by the
    Similar Papers recommendation endpoint.

    This shape matches the existing PaperCard /
    PaperDetailPage expectations.

    embedding is intentionally NOT included.
    """

    paper_id: int
    paper_name: str

    publication_year: Optional[int] = None

    cited_by_count: int = 0

    doi: Optional[str] = None

    abstract: Optional[str] = None

    authors: List[dict] = []

    topics: List[dict] = []


# ============================================================
# Author Recommendation
# ============================================================


class RecommendationAuthor(BaseModel):
    """
    Top author representation.
    """

    author_id: int
    author_name: str
    paper_count: int
    citation_count: int


# ============================================================
# Topic Recommendation
# ============================================================


class RecommendationTopic(BaseModel):
    """
    Topic summary.
    """

    topic_id: int
    topic_name: str
    paper_count: int


# ============================================================
# Topic Papers
# ============================================================


class TopicPapersResponse(BaseModel):
    """
    Paginated papers belonging to a topic.
    """

    topic_id: int
    topic_name: str

    page: int
    limit: int

    total: int
    total_pages: int

    has_previous: bool
    has_next: bool

    results: List[RecommendationPaper]