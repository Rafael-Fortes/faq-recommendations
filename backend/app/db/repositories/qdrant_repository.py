from qdrant_client import QdrantClient, models
from app.config.constants import QDRANT_URL
from app.utils.logger import Logger
import uuid
from typing import Dict, List, Any, Optional

class QdrantRepository:
    def create_collection(self, client: QdrantClient, collection_name: str, vector_size: int, distance: str) -> None:
        Logger.info(f"Checking if collection '{collection_name}' exists")
        if self._check_collection_exists(client, collection_name):
            Logger.error(f"Collection '{collection_name}' already exists")
            raise ValueError(f"Collection {collection_name} already exists")
        try:
            Logger.info(f"Creating collection '{collection_name}' with vector size {vector_size} and distance {distance}")
            if distance == "cosine":
                distance = models.Distance.COSINE
            elif distance == "euclidean":
                distance = models.Distance.EUCLID
            else:
                Logger.error(f"Invalid distance: {distance}")
                raise ValueError(f"Invalid distance: {distance}")

            vectors_config = models.VectorParams(size=vector_size, distance=distance)
            client.create_collection(collection_name, vectors_config=vectors_config)
            Logger.info(f"Collection '{collection_name}' successfully created")
        except Exception as e:
            Logger.error(f"Error creating collection '{collection_name}': {str(e)}")
            raise e


    def _check_collection_exists(self, client: QdrantClient, collection_name: str) -> bool:
        try:
            exists = client.collection_exists(collection_name)
            Logger.debug(f"Collection '{collection_name}' exists: {exists}")
            return exists
        except Exception as e:
            Logger.error(f"Error checking if collection '{collection_name}' exists: {str(e)}")
            raise e
    

    def delete_collection(self, client: QdrantClient, collection_name: str) -> None:
        try:
            Logger.info(f"Attempting to delete collection '{collection_name}'")
            if not self._check_collection_exists(client, collection_name):
                Logger.error(f"Collection '{collection_name}' does not exist")
                raise ValueError(f"Collection {collection_name} does not exist")
            client.delete_collection(collection_name)
            Logger.info(f"Collection '{collection_name}' successfully deleted")
        except Exception as e:
            Logger.error(f"Error deleting collection '{collection_name}': {str(e)}")
            raise e
    
    def get_collection_info(self, client: QdrantClient, collection_name: str) -> dict:
        try:
            Logger.info(f"Getting information for collection '{collection_name}'")
            if not self._check_collection_exists(client, collection_name):
                Logger.error(f"Collection '{collection_name}' does not exist")
                raise ValueError(f"Collection {collection_name} does not exist")
            collection_info = client.get_collection(collection_name)
            metadata = {
                "name": collection_name,
                "vector_size": collection_info.config.params.vectors.size,
                "distance": str(collection_info.config.params.vectors.distance),
                "points_count": collection_info.points_count
            }
            Logger.info(f"Successfully retrieved information for collection '{collection_name}'")
            Logger.debug(f"Collection metadata: {metadata}")
            return metadata
        except Exception as e:
            Logger.error(f"Error getting collection information for '{collection_name}': {str(e)}")
            raise e
    
    def add_point(self, client: QdrantClient, collection_name: str, vector: List[float], payload: Dict[str, Any]) -> str:
        try:
            # First check if collection exists
            Logger.info(f"Checking if collection '{collection_name}' exists before adding point")
            if not self._check_collection_exists(client, collection_name):
                Logger.error(f"Collection '{collection_name}' does not exist")
                raise ValueError(f"Collection {collection_name} does not exist")
            
            # Generate a unique ID for the point
            point_id = str(uuid.uuid4())
            Logger.info(f"Adding point with ID '{point_id}' to collection '{collection_name}'")
            
            # Create the point
            point = models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            )
            
            # Add the point to the collection
            client.upsert(
                collection_name=collection_name,
                points=[point]
            )
            
            Logger.info(f"Point '{point_id}' successfully added to collection '{collection_name}'")
            return point_id
            
        except Exception as e:
            Logger.error(f"Error adding point to collection '{collection_name}': {str(e)}")
            raise e
            
    def get_points(self, client: QdrantClient, collection_name: str, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """
        Retrieve points from a collection with pagination
        """
        try:
            Logger.info(f"Retrieving points from collection '{collection_name}'")
            
            # Check if collection exists
            if not self._check_collection_exists(client, collection_name):
                Logger.error(f"Collection '{collection_name}' does not exist")
                raise ValueError(f"Collection {collection_name} does not exist")
            
            # Get collection info to determine the total number of points
            collection_info = client.get_collection(collection_name)
            total_points = collection_info.points_count
            
            # Determine the limit to use
            if limit is None:
                actual_limit = total_points
            else:
                actual_limit = min(limit, total_points - offset)
                
            if actual_limit <= 0:
                Logger.info(f"No points to retrieve from collection '{collection_name}' with offset {offset}")
                return []
                
            Logger.info(f"Retrieving {actual_limit} points from collection '{collection_name}' starting at offset {offset}")
            
            # Scroll through all points in the collection
            points = []
            scroll_result = client.scroll(
                collection_name=collection_name,
                limit=actual_limit,
                offset=offset,
                with_payload=True,
                with_vectors=False  # We don't need the vectors for display
            )
            
            # Extract the points from the scroll result
            points = [
                {
                    "id": str(point.id),
                    "question": point.payload.get("question", ""),
                    "answer": point.payload.get("answer", "")
                }
                for point in scroll_result[0]
            ]
            
            Logger.info(f"Successfully retrieved {len(points)} points from collection '{collection_name}'")
            return points
            
        except Exception as e:
            Logger.error(f"Error retrieving points from collection '{collection_name}': {str(e)}")
            raise e
        
    def list_collections(self, client: QdrantClient) -> List[str]:
        """
        Get a list of all collection names
        """
        try:
            Logger.info("Retrieving list of all collections")
            collections = client.get_collections().collections
            collection_names = [collection.name for collection in collections]
            Logger.info(f"Retrieved {len(collection_names)} collections")
            return collection_names
        except Exception as e:
            Logger.error(f"Error retrieving collections list: {str(e)}")
            raise e
    
    def search_points(self, client: QdrantClient, collection_name: str, query_vector: list[float], limit: int = 5) -> List[Dict]:
        try:
            Logger.info(f"Searching for points in collection '{collection_name}' with query: {query_vector[:5]}...")

            # Check if collection exists
            if not self._check_collection_exists(client, collection_name):
                Logger.error(f"Collection '{collection_name}' does not exist")
                raise ValueError(f"Collection {collection_name} does not exist")
            
            # Search for points in the collection
            search_result = client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )

            # Convert search results to list of dictionaries
            results = [
                {
                    "id": str(hit.id),
                    "question": hit.payload.get("question", ""),
                    "answer": hit.payload.get("answer", ""),
                    "score": hit.score
                }
                for hit in search_result
            ]

            Logger.info(f"Successfully found {len(results)} points in collection '{collection_name}'")
            return results
            
        except Exception as e:
            Logger.error(f"Error searching for points in collection '{collection_name}': {str(e)}")
            raise e
