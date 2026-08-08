from typing import List

from pydantic import BaseModel, ConfigDict


class TopicListResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )


class TopicPaperResponse(BaseModel):
    id: int
    title: str
    publication_year: int | None = None
    cited_by_count: int | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class TopicDetailResponse(BaseModel):
    id: int
    name: str
    papers: List[TopicPaperResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )


class PaginatedTopicResponse(BaseModel):
    page: int
    page_size: int
    total: int
    results: List[TopicListResponse]

