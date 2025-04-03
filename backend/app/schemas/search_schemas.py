from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.base_schemas import BaseResponse


class SearchResultItem(BaseModel):
    """
    Represents a single search result item
    """
    id: str = Field(..., description="ID of the FAQ item")
    question: str = Field(..., description="The question from the FAQ")
    answer: str = Field(..., description="The answer from the FAQ")
    score: float = Field(..., description="Similarity score (0-1)")


class SearchRequest(BaseModel):
    """
    Request schema for searching FAQs
    """
    question: str = Field(..., description="The question to search for")
    faq_name: str = Field(..., description="The name of the FAQ to search in")
    limit: int = Field(5, description="Maximum number of results to return", ge=1, le=50)


class SearchResponse(BaseResponse):
    """
    Response schema for search results
    """
    data: List[SearchResultItem] = Field(default_factory=list, description="List of search results") 