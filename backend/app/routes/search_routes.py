from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional

from app.schemas.search_schemas import SearchRequest, SearchResponse
from app.services.search_service import SearchService
from app.utils.logger import Logger

router = APIRouter(tags=["FAQ Search"])

search_service = SearchService()

@router.post("/", response_model=SearchResponse)
async def search_faqs(request: SearchRequest):
    """
    Search for FAQs based on a question
    """
    try:
        Logger.info(f"Received search request for question: '{request.question}'")
        search_results = search_service.search_faqs(
            question=request.question,
            faq_name=request.faq_name, 
            limit=request.limit
        )
        
        Logger.info(f"Successfully retrieved {len(search_results)} search results")
        return SearchResponse(
            message=f"Found {len(search_results)} similar FAQ(s)",
            data=search_results
        )
    except ValueError as ve:
        Logger.error(f"Value error in search_faqs endpoint: {str(ve)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except HTTPException as he:
        raise he
    except Exception as e:
        Logger.error(f"Error in search_faqs endpoint: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to search FAQs: {str(e)}")