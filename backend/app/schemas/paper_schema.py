from typing import List, Optional

from pydantic import BaseModel, ConfigDict



# =====================================================
# Author Response
# =====================================================

class AuthorResponse(BaseModel):

    id: int

    name: str


    model_config = ConfigDict(
        from_attributes=True
    )



# =====================================================
# Topic Response
# =====================================================

class TopicResponse(BaseModel):

    id: int

    name: str


    model_config = ConfigDict(
        from_attributes=True
    )



# =====================================================
# Paper List Response
# Used for search results page
# =====================================================

class PaperListResponse(BaseModel):

    id: int

    title: str

    publication_year: Optional[int] = None

    cited_by_count: Optional[int] = 0


    model_config = ConfigDict(
        from_attributes=True
    )



# =====================================================
# Paper Detail Response
# Used for paper detail page
# =====================================================

class PaperDetailResponse(BaseModel):

    id: int

    title: str

    abstract: Optional[str] = None

    publication_year: Optional[int] = None

    doi: Optional[str] = None

    cited_by_count: Optional[int] = 0


    authors: List[AuthorResponse] = []

    topics: List[TopicResponse] = []


    model_config = ConfigDict(
        from_attributes=True
    )



# =====================================================
# Pagination Response
# Used for GET /papers
# =====================================================

class PaginatedPaperResponse(BaseModel):

    page: int

    page_size: int

    total: int

    results: List[PaperListResponse]


    model_config = ConfigDict(
        from_attributes=True
    )