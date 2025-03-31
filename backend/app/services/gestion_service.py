from fastapi import UploadFile, HTTPException
from app.db.session import get_db
from app.db.repositories.gestion_repository import GestionRepository
from app.core.semantic_engine import SemanticEngine
import pandas as pd
from typing import List, Dict, Any, Optional
import io


class GestionService:
    def __init__(self):
        self.gestion_repository = GestionRepository()
        self.semantic_engine = SemanticEngine(model_name="all-MiniLM-L6-v2")

    def get_faq_embeddings(self, faq_df: pd.DataFrame) -> list[dict]:
        try:	
            faq_df_embedded = self.semantic_engine.embed_dataframe_column(faq_df, "Question")
            return faq_df_embedded.to_dict(orient="records")
        except Exception as e:
            print(e)
            raise e

    async def ingest_faq(self, file: UploadFile, client_name: str, faq_name: str, separator: str) -> Dict[str, Any]:
        """Ingest a CSV file containing FAQs into the database"""
        try:
            # Read the file content and convert to dataframe
            contents = await file.read()
            faq_df = pd.read_csv(io.StringIO(contents.decode("utf-8")), sep=separator)
            
            # Validate required columns
            required_columns = ["Question", "Answer"]
            missing_columns = [col for col in required_columns if col not in faq_df.columns]
            if missing_columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required columns: {', '.join(missing_columns)}"
                )
            
            # Generate embeddings for the questions
            faq_df_embedded_dict = self.get_faq_embeddings(faq_df)
            
            # Store in MongoDB
            with get_db(client_name) as db:
                # Check if FAQ with this name already exists
                existing_collection = self.gestion_repository.verify_collection_exists(db, faq_name)
                
                if existing_collection:
                    # Delete the existing collection, create a new one and insert the new data
                    self.gestion_repository.delete_collection(db, faq_name)
                    self.gestion_repository.insert_many_dicts(db, faq_name, faq_df_embedded_dict)
                    self.gestion_repository.update_one(
                        db, 
                        "faq_metadata", 
                        {"name": client_name},
                        {"$set": {"count": len(faq_df_embedded_dict), "updated_at": pd.Timestamp.now()}}
                    )
                else:
                    # Create new FAQ
                    self.gestion_repository.insert_many_dicts(db, faq_name, faq_df_embedded_dict)
                    self.gestion_repository.insert_one_dict(
                        db,
                        "faq_metadata",
                        {
                            "name": client_name,
                            "count": len(faq_df_embedded_dict),
                            "created_at": pd.Timestamp.now(),
                            "updated_at": pd.Timestamp.now()
                        }
                    )
                
                await file.seek(0)
                
                return {
                    "count": len(faq_df_embedded_dict),
                    "is_new": not existing_collection
                }
                
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Error in ingest_faq: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while ingesting FAQ")


    async def list_faqs(self, client_name: str) -> List[Dict[str, Any]]:
        """List all available FAQs with their metadata"""
        try:
            with get_db(client_name) as db:
                # Check if client exists
                client_exists = self.gestion_repository.verify_collection_exists(db, client_name)
                
                log = {
                    "client_name": client_name,
                    "client_exists": client_exists
                }
                print(log)

                if not client_exists:
                    raise HTTPException(status_code=404, detail="Client not found")
                
                faqs = self.gestion_repository.find_many(db, "faq_metadata", {})
                return [{
                    "name": faq.get("name"),
                    "count": faq.get("count"),
                    "created_at": faq.get("created_at").isoformat() if faq.get("created_at") else "",
                    "updated_at": faq.get("updated_at").isoformat() if faq.get("updated_at") else ""
                } for faq in faqs]
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Error in list_faqs: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while listing FAQs")
            
    async def create_faq(self, client_name: str, faq_name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new FAQ collection"""
        try:
            with get_db(client_name) as db:
                # Check if FAQ already exists
                if self.gestion_repository.verify_collection_exists(db, faq_name):
                    raise HTTPException(status_code=400, detail=f"FAQ '{faq_name}' already exists")
                
                # Create metadata entry
                metadata = {
                    "name": faq_name,
                    "description": description,
                    "count": 0,
                    "created_at": pd.Timestamp.now(),
                    "updated_at": pd.Timestamp.now()
                }
                self.gestion_repository.insert_one_dict(db, "faq_metadata", metadata)
                
                return metadata
                
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Error in create_faq: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while creating FAQ")

    async def add_faq_item(self, client_name: str, faq_name: str, question: str, answer: str) -> Dict[str, Any]:
        """Add a new item to an existing FAQ"""
        try:
            with get_db(client_name) as db:
                # Check if FAQ exists
                if not self.gestion_repository.verify_collection_exists(db, faq_name):
                    raise HTTPException(status_code=404, detail=f"FAQ '{faq_name}' not found")
                
                # Generate embedding for the question
                question_embedding = self.semantic_engine.embed_text(question)
                
                # Create FAQ item
                faq_item = {
                    "question": question,
                    "answer": answer,
                    "embedding": question_embedding
                }
                
                # Insert the item
                self.gestion_repository.insert_one_dict(db, faq_name, faq_item)
                
                # Update metadata count
                self.gestion_repository.update_one(
                    db,
                    "faq_metadata",
                    {"name": faq_name},
                    {"$inc": {"count": 1}, "$set": {"updated_at": pd.Timestamp.now()}}
                )
                
                return faq_item
                
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Error in add_faq_item: {str(e)}")
            raise HTTPException(status_code=500, detail="Error while adding FAQ item")
            
