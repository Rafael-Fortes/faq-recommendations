import io
from typing import Any, List, Optional, Dict, Tuple
from app.utils.logger import Logger
import pandas as pd
from fastapi import HTTPException, UploadFile
from app.core.models import SemanticEngine
from app.db.repositories.qdrant_repository import QdrantRepository
from app.db.session import get_qdrant_client
from app.schemas.gestion_schemas import Distance, FaqItem, FaqImportData, FaqListItem
import csv


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

    def add_faq_item(self, faq_name: str, question: str, answer: str) -> FaqItem:
        """Add a new question and answer to an existing FAQ collection"""
        try:
            Logger.info(f"Adding new item to FAQ '{faq_name}'")
            
            # Generate embedding for the question
            Logger.info(f"Generating embedding for question: {question[:50]}..." if len(question) > 50 else f"Generating embedding for question: {question}")
            embedding = self.semantic_engine.embed_text(question)
            
            # Create the FAQ item
            faq_item = FaqItem(
                question=question,
                answer=answer,
                embedding=embedding
            )

            # Payload
            payload = {
                "question": question,
                "answer": answer
            }
            
            # Add the item to the collection
            with get_qdrant_client() as client:
                Logger.info(f"Adding item to Qdrant collection '{faq_name}'")
                point_id = self.qdrant_repository.add_point(
                    client,
                    faq_name,
                    embedding,
                    payload
                )
                Logger.info(f"Item added successfully to FAQ '{faq_name}' with ID: {point_id}")
            
            return faq_item
                
        except HTTPException as he:
            Logger.error(f"HTTPException in add_faq_item: {str(he)}")
            raise he
        except Exception as e:
            Logger.error(f"Error in add_faq_item: {str(e)}")
            raise e
            
    def import_faq_from_csv(self, faq_name: str, file: UploadFile) -> FaqImportData:
        """Import FAQ items from a CSV file into an existing FAQ collection"""
        try:
            Logger.info(f"Starting import of FAQ items from CSV to '{faq_name}'")
            
            # Check if the FAQ exists
            with get_qdrant_client() as client:
                if not self.qdrant_repository._check_collection_exists(client, faq_name):
                    Logger.error(f"Collection '{faq_name}' does not exist")
                    raise ValueError(f"FAQ '{faq_name}' does not exist. Please create it first.")
            
            # Read the CSV file
            Logger.info(f"Reading CSV file: {file.filename}")
            contents = file.file.read()
            buffer = io.StringIO(contents.decode('utf-8'))
            
            # Load CSV into pandas DataFrame
            try:
                # Read CSV with pandas
                df = pd.read_csv(buffer)
                
                # Convert column names to lowercase for case-insensitive matching
                df.columns = [col.lower() for col in df.columns]
                
                # Check if required columns exist
                required_columns = ["question", "answer"]
                if not all(col in df.columns for col in required_columns):
                    missing_cols = [col for col in required_columns if col not in df.columns]
                    Logger.error(f"CSV file is missing required columns: {missing_cols}")
                    raise ValueError(f"CSV file is missing required columns: {missing_cols}")
                
                # Clean up data
                Logger.info("Cleaning data before processing")
                df['question'] = df['question'].str.strip()
                df['answer'] = df['answer'].str.strip()
                
                # Remove rows with empty questions or answers
                original_row_count = len(df)
                df = df.dropna(subset=['question', 'answer'])
                df = df[(df['question'] != '') & (df['answer'] != '')]
                dropped_rows = original_row_count - len(df)
                
                if dropped_rows > 0:
                    Logger.warning(f"Dropped {dropped_rows} rows with empty questions or answers")
                
                if len(df) == 0:
                    Logger.error("No valid data found in CSV file after cleaning")
                    raise ValueError("No valid questions and answers found in the CSV file")
                
                # Generate embeddings for all questions at once
                Logger.info(f"Generating embeddings for {len(df)} questions")
                df_with_embeddings = self.semantic_engine.embed_dataframe_column(df, 'question')
                Logger.info("Embeddings generated successfully")
                
                # Add points to Qdrant collection
                Logger.info(f"Adding {len(df_with_embeddings)} items to collection '{faq_name}'")
                
                items_count = 0
                failed_count = 0
                
                with get_qdrant_client() as client:
                    for _, row in df_with_embeddings.iterrows():
                        try:
                            # Create payload
                            payload = {
                                "question": row['question'],
                                "answer": row['answer']
                            }
                            
                            # Add point to collection
                            self.qdrant_repository.add_point(
                                client,
                                faq_name,
                                row['embedding'],
                                payload
                            )
                            
                            items_count += 1
                            
                            # Log progress periodically
                            if items_count % 50 == 0:
                                Logger.info(f"Added {items_count}/{len(df_with_embeddings)} items to FAQ '{faq_name}'")
                                
                        except Exception as item_error:
                            Logger.error(f"Error adding item from CSV: {str(item_error)}")
                            failed_count += 1
                
                # Create import result
                import_data = FaqImportData(
                    faq_name=faq_name,
                    filename=file.filename,
                    items_count=items_count,
                    failed_count=failed_count,
                    status="completed"
                )
                
                Logger.info(f"CSV import completed for FAQ '{faq_name}'. Imported: {items_count}, Failed: {failed_count}")
                return import_data
                
            except pd.errors.ParserError as parser_error:
                Logger.error(f"Error parsing CSV file: {str(parser_error)}")
                raise ValueError(f"Invalid CSV format: {str(parser_error)}")
                
        except ValueError as ve:
            Logger.error(f"Value error in import_faq_from_csv: {str(ve)}")
            raise ve
        except HTTPException as he:
            Logger.error(f"HTTPException in import_faq_from_csv: {str(he)}")
            raise he
        except Exception as e:
            Logger.error(f"Error in import_faq_from_csv: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to import CSV: {str(e)}")
        finally:
            # Close the file
            file.file.close()
            Logger.info("CSV file closed")
            
    def get_faq_items(self, faq_name: str, limit: Optional[int] = None, offset: int = 0) -> List[FaqListItem]:
        """
        Retrieve FAQ items from a collection with pagination
        """
        try:
            Logger.info(f"Retrieving FAQ items from '{faq_name}'")
            
            with get_qdrant_client() as client:
                # Check if collection exists
                if not self.qdrant_repository._check_collection_exists(client, faq_name):
                    Logger.error(f"Collection '{faq_name}' does not exist")
                    raise ValueError(f"FAQ '{faq_name}' does not exist")
                
                # Get points from the collection
                points = self.qdrant_repository.get_points(client, faq_name, limit, offset)
                
                # Convert to FaqListItem objects
                faq_items = [
                    FaqListItem(
                        id=point["id"],
                        question=point["question"],
                        answer=point["answer"]
                    )
                    for point in points
                ]
                
                Logger.info(f"Successfully retrieved {len(faq_items)} items from FAQ '{faq_name}'")
                return faq_items
                
        except ValueError as ve:
            Logger.error(f"Value error in get_faq_items: {str(ve)}")
            raise ve
        except Exception as e:
            Logger.error(f"Error retrieving FAQ items: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to retrieve FAQ items: {str(e)}")