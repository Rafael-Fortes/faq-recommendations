from pydantic import BaseModel, Field
from app.schemas.base_schemas import BaseResponse
from typing import List, Dict, Optional


class FaqImportData(BaseModel):
    faq_name: str
    filename: str
    count: Optional[int] = None


class IngestFaqResponse(BaseResponse):
    data: FaqImportData = Field(default_factory=dict)


class FaqMetadata(BaseModel):
    name: str
    count: int
    created_at: str
    updated_at: str


class FaqItem(BaseModel):
    question: str
    answer: str
    embedding: Optional[List[float]] = None


class FaqListResponse(BaseResponse):
    data: List[FaqMetadata] = Field(default_factory=list)


class FaqDetailResponse(BaseResponse):
    data: Dict[str, List[FaqItem]] = Field(default_factory=dict)

