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

    author_id: int
    author_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Topic Response
# ============================================================

class TopicResponse(BaseModel):

    topic_id: int
    topic_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper List Response
# ============================================================

class PaperListResponse(BaseModel):

    paper_id: int
    paper_name: str

    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = 0

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper Detail Response
# ============================================================

class PaperDetailResponse(BaseModel):

    paper_id: int
    paper_name: str

    abstract: Optional[str] = None
    publication_year: Optional[int] = None
    doi: Optional[str] = None
    cited_by_count: Optional[int] = 0

    authors: List[AuthorResponse] = Field(
        default_factory=list
    )

    topics: List[TopicResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paginated Paper Response
# ============================================================

class PaginatedPaperResponse(BaseModel):

    page: int
    page_size: int
    total: int

    results: List[PaperListResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paper Collection Response
# ============================================================

class PaperCollectionResponse(BaseModel):
    """
    Response containing multiple paper details.
    """

    results: List[PaperDetailResponse] = Field(
        default_factory=list
    )

    requested_count: int = Field(
        ge=0,
        description="Number of paper IDs requested.",
    )

    returned_count: int = Field(
        ge=0,
        description="Number of papers found.",
    )

    model_config = ConfigDict(
        from_attributes=True
    )
