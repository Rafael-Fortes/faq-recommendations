from typing import List, Optional
from app.utils.logger import Logger
from app.core.models import SemanticEngine
from app.db.repositories.qdrant_repository import QdrantRepository
from app.db.session import get_qdrant_client
from app.schemas.search_schemas import SearchResultItem
from fastapi import HTTPException


class SearchService:
    def __init__(self):
        Logger.info("Initializing SearchService")
        self.qdrant_repository = QdrantRepository()
        self.semantic_engine = SemanticEngine(model_name="all-MiniLM-L6-v2")

    def search_faqs(self, question: str, faq_name: str, limit: int = 5) -> List[SearchResultItem]:
        """
        Search for similar FAQs based on a question
        """
        try:
            Logger.info(f"Searching for: '{question}'")
            
            # Generate embedding for the question
            question_embedding = self.semantic_engine.embed_text(question)
            Logger.info(f"Generated embedding for question: '{question[:50]}...'")
            
            with get_qdrant_client() as client:    
                # Search in the specified collection
                Logger.info(f"Searching in FAQ collection: '{faq_name}'")
                search_result = self.qdrant_repository.search_points(client, faq_name, question_embedding, limit)
                
                Logger.info(f"Found {len(search_result)} results in collection '{faq_name}'")
                return [SearchResultItem(**result) for result in search_result]
                    
        except ValueError as ve:
            Logger.error(f"Value error in search_faqs: {str(ve)}")
            raise ve
        except Exception as e:
            Logger.error(f"Error in search_faqs: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to search FAQs: {str(e)}") 