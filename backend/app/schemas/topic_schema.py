from typing import List, Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# Topic List Response
# ============================================================

class TopicListResponse(BaseModel):

    topic_id: int

    topic_name: str

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Topic Paper Response
# ============================================================

class TopicPaperResponse(BaseModel):

    paper_id: int

    paper_name: str

    publication_year: Optional[int] = None

    cited_by_count: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Topic Detail Response
# ============================================================

class TopicDetailResponse(BaseModel):

    topic_id: int

    topic_name: str

    papers: List[TopicPaperResponse] = []

    model_config = ConfigDict(
        from_attributes=True
    )


# ============================================================
# Paginated Topic Response
# ============================================================

class PaginatedTopicResponse(BaseModel):

    page: int

    page_size: int

    total: int

    results: List[TopicListResponse]

    model_config = ConfigDict(
        from_attributes=True
    )