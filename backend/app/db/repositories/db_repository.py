from pymongo import MongoClient


class DBRepository:
    def __init__(self):
        pass
    
    def verify_collection_exists(self, db: MongoClient, collection_name: str):
        try:
            return collection_name in db.list_collection_names()
        except Exception as e:
            raise e
            
    def delete_collection(self, db: MongoClient, collection_name: str):
        try:
            db.drop_collection(collection_name)
        except Exception as e:
            raise e
