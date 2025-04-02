from qdrant_client import QdrantClient, models
from app.config.constants import QDRANT_URL
from app.utils.logger import Logger

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
            self._check_collection_exists(client, collection_name)
            client.delete_collection(collection_name)
            Logger.info(f"Collection '{collection_name}' successfully deleted")
        except Exception as e:
            Logger.error(f"Error deleting collection '{collection_name}': {str(e)}")
            raise e
    
    def get_collection_info(self, client: QdrantClient, collection_name: str) -> dict:
        try:
            Logger.info(f"Getting information for collection '{collection_name}'")
            self._check_collection_exists(client, collection_name)
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
        
        


