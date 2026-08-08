from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# Author Summary
# ============================================================

class AuthorListResponse(BaseModel):
    id: int
    name: str
    orcid: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Author Paper
# ============================================================

class AuthorPaperResponse(BaseModel):
    id: int
    title: str
    publication_year: Optional[int] = None
    cited_by_count: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Author Details
# ============================================================

class AuthorDetailResponse(BaseModel):
    id: int
    name: str
    orcid: Optional[str] = None
    papers: List[AuthorPaperResponse] = []

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
    results: List[AuthorListResponse]
