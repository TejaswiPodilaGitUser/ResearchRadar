from typing import List, Optional

from pydantic import BaseModel



class AuthorResponse(BaseModel):

    id: int
    name: str

    class Config:
        from_attributes = True



class TopicResponse(BaseModel):

    id: int
    name: str

    class Config:
        from_attributes = True



class PaperListResponse(BaseModel):

    id: int
    title: str
    publication_year: Optional[int]
    cited_by_count: Optional[int]

    class Config:
        from_attributes = True



class PaperDetailResponse(BaseModel):

    id: int
    title: str
    abstract: Optional[str]
    publication_year: Optional[int]
    doi: Optional[str]

    authors: List[AuthorResponse]

    topics: List[TopicResponse]


    class Config:
        from_attributes = True



class PaginatedPaperResponse(BaseModel):

    page: int
    size: int
    total: int

    results: List[PaperListResponse]