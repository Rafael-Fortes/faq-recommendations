from pymongo import MongoClient


class DBRepository:
    def __init__(self):
        pass
    
    def verify_collection_exists(self, db: MongoClient, collection_name: str):
        try:
            list_collection_names = db.list_collection_names()
            result = collection_name in list_collection_names
            log = {
                "list_collection_names": list_collection_names,
                "collection_name": collection_name,
                "result": result
            }
            print(log)
            return result
        except Exception as e:
            raise e
            
    def delete_collection(self, db: MongoClient, collection_name: str):
        try:
            db.drop_collection(collection_name)
        except Exception as e:
            raise e
