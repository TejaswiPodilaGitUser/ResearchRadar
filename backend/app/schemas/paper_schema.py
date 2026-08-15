from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# ============================================================
# Author Response
# ============================================================

class AuthorResponse(BaseModel):
    """
    Author information returned as part of a paper.
    """

    author_id: int
    author_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Topic Response
# ============================================================

class TopicResponse(BaseModel):
    """
    Topic information returned as part of a paper.
    """

    topic_id: int
    topic_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper List Response
# ============================================================

class PaperListResponse(BaseModel):
    """
    Paper representation used by the
    paginated paper listing endpoint.
    """

    paper_id: int
    paper_name: str

    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = 0

    authors: List[AuthorResponse] = Field(
        default_factory=list,
        description="Authors associated with the paper.",
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper Detail Response
# ============================================================

class PaperDetailResponse(BaseModel):
    """
    Complete paper information.

    Used by:
        - Single paper lookup
        - Paper lookup by name
        - Paper collections
    """

    paper_id: int
    paper_name: str

    abstract: Optional[str] = None
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    cited_by_count: Optional[int] = 0

    authors: List[AuthorResponse] = Field(
        default_factory=list,
        description="Authors associated with the paper.",
    )

    topics: List[TopicResponse] = Field(
        default_factory=list,
        description="Topics associated with the paper.",
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paginated Paper Response
# ============================================================

class PaginatedPaperResponse(BaseModel):
    """
    Paginated response for the paper search/list endpoint.
    """

    page: int = Field(
        ge=1,
        description="Current page number.",
    )

    page_size: int = Field(
        ge=1,
        description="Number of papers returned per page.",
    )

    total: int = Field(
        ge=0,
        description="Total number of matching papers.",
    )

    results: List[PaperListResponse] = Field(
        default_factory=list,
        description="Papers returned for the current page.",
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper Collection Response
# ============================================================

class PaperCollectionResponse(BaseModel):
    """
    Response containing multiple paper details.

    Supports collections retrieved by either:
        - Paper IDs
        - Paper names

    The response preserves the order of the requested
    collection where possible.
    """

    results: List[PaperDetailResponse] = Field(
        default_factory=list,
        description="Papers found in the requested collection.",
    )

    requested_count: int = Field(
        ge=0,
        description="Number of unique papers requested.",
    )

    returned_count: int = Field(
        ge=0,
        description="Number of papers successfully found.",
    )

    model_config = ConfigDict(
        from_attributes=True
    )