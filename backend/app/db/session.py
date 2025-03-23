from pymongo import MongoClient
from app.config.constants import MONGO_URI
from contextlib import contextmanager


@contextmanager
def get_db(db_name: str):
    client = MongoClient(MONGO_URI)
    db = client[db_name]
    yield db
    client.close()

