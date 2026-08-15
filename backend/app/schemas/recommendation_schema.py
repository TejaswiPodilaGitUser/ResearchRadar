from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# ============================================================
# Recommendation Author
# ============================================================

class RecommendationAuthorResponse(BaseModel):

    author_id: int
    author_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Recommendation Topic
# ============================================================

class RecommendationTopicResponse(BaseModel):

    topic_id: int
    topic_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Recommended Paper
# ============================================================

class RecommendationPaperResponse(BaseModel):

    paper_id: int
    paper_name: str

    abstract: Optional[str] = None
    publication_year: Optional[int] = None
    publication_date: Optional[str] = None
    doi: Optional[str] = None
    cited_by_count: Optional[int] = None

    authors: List[RecommendationAuthorResponse] = Field(
        default_factory=list
    )

    topics: List[RecommendationTopicResponse] = Field(
        default_factory=list
    )


# ============================================================
# Recommendation List
# ============================================================

class RecommendationListResponse(BaseModel):

    results: List[RecommendationPaperResponse]


# ============================================================
# Trending Paper
# ============================================================

class TrendingPaperResponse(BaseModel):

    paper_id: int
    paper_name: str

    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Emerging Topic
# ============================================================

class EmergingTopicResponse(BaseModel):

    topic_id: int
    topic_name: str

    paper_count: int
    recent_paper_count: int
    citation_count: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Topic Paper Pagination
# ============================================================

class TopicPaperPageResponse(BaseModel):

    topic_id: int
    topic_name: str

    page: int
    limit: int

    total: int
    total_pages: int

    has_previous: bool
    has_next: bool

    results: List[RecommendationPaperResponse] = Field(
        default_factory=list
    )