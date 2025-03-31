from pydantic import BaseModel, Field, field_validator
from app.schemas.base_schemas import BaseResponse
from typing import List, Dict, Optional


class ClientName(Field):
    client_name: str

    @field_validator('client_name')
    def validate_client_name(cls, v):
        if not v:
            raise ValueError('Client name is required')
        return v

class FaqName(Field):
    faq_name: str

@field_validator('faq_name')
def validate_faq_name(cls, v):
    if not v:
        raise ValueError('FAQ name is required')
    return v


class FaqImportData(BaseModel):
    faq_name: FaqName
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

class FaqListRequest(BaseModel):
    client_name: ClientName


class FaqListResponse(BaseResponse):
    data: List[FaqMetadata] = Field(default_factory=list)


class FaqDetailResponse(BaseResponse):
    data: Dict[str, List[FaqItem]] = Field(default_factory=dict)


class CreateFaqRequest(BaseModel):
    client_name: str
    faq_name: str
    description: Optional[str] = None


class AddFaqItemRequest(BaseModel):
    question: str
    answer: str


class CreateFaqResponse(BaseResponse):
    data: FaqMetadata = Field(default_factory=dict)


class AddFaqItemResponse(BaseResponse):
    data: FaqItem = Field(default_factory=dict)

