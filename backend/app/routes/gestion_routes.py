from fastapi import APIRouter, HTTPException, status, File, Form
from fastapi import UploadFile
from app.schemas.gestion_schemas import IngestFaqResponse, FaqImportData, FaqListResponse, FaqDetailResponse
from app.services.gestion_service import GestionService
import json

router = APIRouter(tags=["Gestion"])

gestion_service = GestionService()

@router.post("/faq/import", response_model=IngestFaqResponse, status_code=status.HTTP_201_CREATED)
async def import_faq(
    file: UploadFile = File(...),
    client_name: str = Form(...),
    faq_name: str = Form(...),
    separator: str = Form(",")
):
    """
    Import a CSV file containing FAQs.
    
    - **file**: CSV file with questions and answers
    - **client_name**: Name of the client to be created or updated
    - **faq_name**: Name of the FAQ to be created or updated
    - **separator**: CSV separator (default: comma)
    
    The CSV file must have at least two columns:
    - 'Question': The FAQ question
    - 'Answer': The corresponding answer
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are allowed"
        )
    
    try:
        result = await gestion_service.ingest_faq(file, client_name, faq_name, separator)
        return IngestFaqResponse(
            message=f"FAQ '{faq_name}' successfully imported for client '{client_name}'",
            data=FaqImportData(
                faq_name=faq_name, 
                filename=file.filename,
                count=result.get("count", 0)
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import FAQ: {str(e)}"
        )

@router.get("/faq", response_model=FaqListResponse)
async def list_faqs(client_name: str):
    """
    List all available FAQs with their metadata.

    - **client_name**: Name of the client to retrieve FAQs from
    """
    try:
        faqs = await gestion_service.list_faqs(client_name)
        return FaqListResponse(
            message="FAQs retrieved successfully",
            data=faqs
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve FAQs: {str(e)}"
        )
