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


class FaqImportData(BaseModel):
    faq_name: NormalizedText
    filename: str
    count: Optional[int] = None


class IngestFaqResponse(BaseResponse):
    data: FaqImportData = Field(default_factory=dict)

class FaqItem(BaseModel):
    question: str
    answer: str
    embedding: Optional[List[float]] = None


class FaqListRequest(BaseModel):
    client_name: NormalizedText


class FaqListResponse(BaseResponse):
    data: List[dict] = Field(default_factory=list)


class FaqDetailResponse(BaseResponse):
    data: Dict[str, List[FaqItem]] = Field(default_factory=dict)


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

