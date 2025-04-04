from fastapi import APIRouter, HTTPException, status, File, Form, UploadFile, Depends, Query
from app.schemas.gestion_schemas import CreateFaqResponse, CreateFaqRequest, AddFaqItemResponse, AddFaqItemRequest, FaqImportResponse, FaqImportRequest, ReadFaqResponse, DeleteFaqResponse, ListFaqsResponse, FaqCollectionInfo
from app.services.gestion_service import GestionService
import json
from typing import Optional, List
from app.utils.logger import Logger

router = APIRouter(tags=["Gestion"])

gestion_service = GestionService()

@router.post("/faq", response_model=CreateFaqResponse, status_code=status.HTTP_201_CREATED)
def create_faq(request: CreateFaqRequest):
    """
    Create a new FAQ collection.
    """
    try:
        result = gestion_service.create_faq(
            request.faq_name,
            request.distance
        )
        return CreateFaqResponse(
            message=f"FAQ '{request.faq_name}' successfully created",
            data=result
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create FAQ: {str(ve)}"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create FAQ: {str(e)}"
        )

@router.post("/faq/{faq_name}/item", response_model=AddFaqItemResponse, status_code=status.HTTP_201_CREATED)
def add_faq_item(faq_name: str, request: AddFaqItemRequest):
    """
    Add a new item (question and answer) to an existing FAQ collection.
    """
    try:
        faq_item = gestion_service.add_faq_item(
            faq_name,
            request.question,
            request.answer
        )
        return AddFaqItemResponse(
            message=f"Item successfully added to FAQ '{faq_name}'",
            data=faq_item
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to add item to FAQ: {str(ve)}"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add item to FAQ: {str(e)}"
        )

@router.post("/faq/{faq_name}/import", response_model=FaqImportResponse, status_code=status.HTTP_200_OK)
def import_faq_from_csv(
    faq_name: str, 
    file: UploadFile = File(...),
):
    """
    Import FAQ items from a CSV file into an existing FAQ collection using Pandas for efficient batch processing.
    The CSV file should have at least two columns named 'Question' and 'Answer'.
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file must be a CSV file"
            )
            
        import_result = gestion_service.import_faq_from_csv(faq_name, file)
        
        return FaqImportResponse(
            message=f"Successfully imported {import_result.items_count} items into FAQ '{faq_name}' with {import_result.failed_count} failures",
            data=import_result
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to import CSV: {str(ve)}"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import CSV: {str(e)}"
        )

@router.get("/faq/{faq_name}/items", response_model=ReadFaqResponse)
def get_faq_items(
    faq_name: str,
    limit: Optional[int] = Query(None, description="Maximum number of items to retrieve"),
    offset: int = Query(0, description="Number of items to skip")
):
    """
    Retrieve FAQ items from a specified FAQ collection.
    """
    try:
        faq_items = gestion_service.get_faq_items(faq_name, limit, offset)
        
        return ReadFaqResponse(
            message=f"Successfully retrieved {len(faq_items)} items from FAQ '{faq_name}'",
            data=faq_items
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve FAQ items: {str(ve)}"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve FAQ items: {str(e)}"
        )

@router.delete("/faq/{faq_name}", response_model=DeleteFaqResponse)
def delete_faq(faq_name: str):
    """
    Delete a FAQ collection.
    
    This endpoint permanently removes a FAQ collection and all its questions and answers.
    The operation cannot be undone.
    """
    try:
        result = gestion_service.delete_faq(faq_name)
        
        return DeleteFaqResponse(
            message=f"Successfully deleted FAQ '{faq_name}' with {result['items_count']} items",
            data=result
        )
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete FAQ: {str(ve)}"
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete FAQ: {str(e)}"
        )

@router.get("/faqs", response_model=ListFaqsResponse)
def list_faqs():
    """
    List all available FAQs
    """
    try:
        Logger.info("Handling request to list all FAQs")
        faqs = gestion_service.list_faqs()
        
        return ListFaqsResponse(
            message=f"Successfully retrieved {len(faqs)} FAQs",
            data=[FaqCollectionInfo(**faq) for faq in faqs]
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        Logger.error(f"Error listing FAQs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list FAQs: {str(e)}"
        )

