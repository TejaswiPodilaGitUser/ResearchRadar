from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


# ============================================================
# Author Summary
# ============================================================

class AuthorListResponse(BaseModel):
    author_id: int
    author_name: str
    orcid: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Author's Paper
# ============================================================

class AuthorPaperResponse(BaseModel):
    paper_id: int
    paper_name: str
    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Author Details
# ============================================================

class AuthorDetailResponse(BaseModel):
    author_id: int
    author_name: str
    orcid: Optional[str] = None

    papers: List[
        AuthorPaperResponse
    ] = Field(
        default_factory=list
    )

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paginated Authors
# ============================================================

class PaginatedAuthorResponse(BaseModel):
    page: int
    page_size: int
    total: int

    results: List[
        AuthorListResponse
    ]


# ============================================================
# Multiple Author Information
# ============================================================

class MultipleAuthorInfo(BaseModel):
    """
    Basic information about one selected author.
    """

    author_id: int
    author_name: str
    orcid: Optional[str] = None


# ============================================================
# Shared Paper
# ============================================================

class SharedPaperResponse(BaseModel):
    """
    A paper associated with two or more
    selected authors.
    """

    paper_id: int
    paper_name: str
    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = None

    author_ids: List[int] = Field(
        default_factory=list
    )

    author_names: List[str] = Field(
        default_factory=list
    )


# ============================================================
# Multiple Author Response
# ============================================================

class MultipleAuthorsResponse(BaseModel):
    """
    Research result for multiple authors.

    Supports multiple authors selected by
    author ID or author name.

    Contains:
      - Selected authors
      - Papers shared by multiple selected authors
      - All papers grouped by author
    """

    # --------------------------------------------------------
    # Selected Authors
    # --------------------------------------------------------

    authors: List[
        MultipleAuthorInfo
    ] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Papers shared by selected authors
    # --------------------------------------------------------

    shared_papers: List[
        SharedPaperResponse
    ] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # All papers grouped by author ID
    #
    # Example:
    #
    # {
    #     "2150": [...],
    #     "1561": [...]
    # }
    # --------------------------------------------------------

    papers_by_author: dict[
        str,
        List[AuthorPaperResponse],
    ] = Field(
        default_factory=dict
    )
