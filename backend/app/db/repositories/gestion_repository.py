from pymongo import MongoClient
from .db_repository import DBRepository


class GestionRepository(DBRepository):
    def __init__(self):
        pass

    def insert_one_dict(self, db: MongoClient, collection_name: str, dict: dict):
        try:
            db[collection_name].insert_one(dict)
        except Exception as e:
            raise e

    def insert_many_dicts(self, db: MongoClient, collection_name: str, dicts: list[dict]):
        try:
            db[collection_name].insert_many(dicts)
        except Exception as e:
            raise e

    def delete_many(self, db: MongoClient, collection_name: str, query: dict):
        try:
            db[collection_name].delete_many(query)
        except Exception as e:
            raise e

    def find_many(self, db: MongoClient, collection_name: str, query: dict):
        try:
            return db[collection_name].find(query)
        except Exception as e:
            raise e

    def update_one(self, db: MongoClient, collection_name: str, query: dict, update: dict):
        try:
            db[collection_name].update_one(query, update)
        except Exception as e:
            raise e
