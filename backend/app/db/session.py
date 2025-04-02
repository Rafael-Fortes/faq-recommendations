from qdrant_client import QdrantClient
from app.config import constants
from contextlib import contextmanager
from app.utils.logger import Logger

@contextmanager
def get_qdrant_client():
    Logger.info("Getting Qdrant client")
    client = QdrantClient(url=constants.QDRANT_URL)
    Logger.info("Qdrant client retrieved successfully")
    yield client
    Logger.info("Closing Qdrant client")
    client.close()