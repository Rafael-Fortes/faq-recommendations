import io
from typing import Any, List, Optional
from app.utils.logger import Logger
import pandas as pd
from fastapi import HTTPException, UploadFile
from app.core.models import SemanticEngine
from app.db.repositories.qdrant_repository import QdrantRepository
from app.db.session import get_qdrant_client
from app.schemas.gestion_schemas import Distance


class GestionService:
    def __init__(self):
        Logger.info("Initializing GestionService")
        self.qdrant_repository = QdrantRepository()
        self.semantic_engine = SemanticEngine(model_name="all-MiniLM-L6-v2")

    def get_faq_embeddings(self, faq_df: pd.DataFrame) -> list[dict]:
        try:	
            Logger.info("Getting FAQ embeddings")
            faq_df_embedded = self.semantic_engine.embed_dataframe_column(faq_df, "Question")
            Logger.info("FAQ embeddings retrieved successfully")
            return faq_df_embedded.to_dict(orient="records")
        except Exception as e:
            Logger.error(f"Error getting FAQ embeddings - {str(e)}")
            raise e
            
    def create_faq(self, faq_name: str, distance: Distance) -> dict:
        """Create a new FAQ collection"""
        try:
            with get_qdrant_client() as client:
                Logger.info("Creating FAQ collection")
                self.qdrant_repository.create_collection(client, faq_name, self.semantic_engine.vector_size, distance)
                Logger.info("FAQ collection created successfully")
                metadata = self.qdrant_repository.get_collection_info(client, faq_name)
                Logger.info("FAQ collection metadata retrieved successfully")
            return metadata
                
        except HTTPException as he:
            Logger.error(f"HTTPException in create_faq: {str(he)}")
            raise he
        except Exception as e:
            Logger.error(f"Error in create_faq: {str(e)}")
            raise e