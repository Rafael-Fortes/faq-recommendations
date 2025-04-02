from pydantic import BaseModel, Field, field_validator, AfterValidator
from app.schemas.base_schemas import BaseResponse
from typing import List, Dict, Optional, Annotated
from enum import Enum


def normalize_text(v: str) -> str:
    """Normalize text by stripping whitespace and lowercasing"""
    if not v:
        raise ValueError("Field is required")
    return v.strip().lower()


NormalizedText = Annotated[str, AfterValidator(normalize_text)]


class FaqItem(BaseModel):
    question: str
    answer: str
    embedding: Optional[List[float]] = None


class FaqListItem(BaseModel):
    """Schema for FAQ items without embeddings, for display purposes"""
    question: str
    answer: str
    id: Optional[str] = None


class Distance(str, Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"


class CreateFaqRequest(BaseModel):
    faq_name: NormalizedText = Field(..., description="The name of the FAQ")
    distance: Distance = Field("cosine", description="The distance metric")


class AddFaqItemRequest(BaseModel):
    question: str
    answer: str


class CreateFaqResponse(BaseResponse):
    data: Dict = Field(default_factory=dict)


class AddFaqItemResponse(BaseResponse):
    data: FaqItem = Field(default_factory=dict)


class FaqImportRequest(BaseModel):
    faq_name: NormalizedText = Field(..., description="The name of the FAQ to import into")


class FaqImportData(BaseModel):
    faq_name: NormalizedText
    filename: str
    items_count: int = 0
    failed_count: int = 0
    status: str = "completed"


class FaqImportResponse(BaseResponse):
    data: FaqImportData = Field(default_factory=dict)


class FaqImportProgressResponse(BaseResponse):
    data: Dict = Field(default_factory=dict)


class ReadFaqResponse(BaseResponse):
    """Response schema for retrieving FAQ items"""
    data: List[FaqListItem] = Field(default_factory=list)


