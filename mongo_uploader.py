from pymongo import MongoClient

class MongoUploader:

    def __init__(self) -> None:
        client = MongoClient('mongodb://localhost:27017/')
        self.db = client["projekt_db"]

    def upload_collection_data(self, collection_name: str, collection_data: dict) -> None:
        collection = self.db[collection_name]
        collection.insert_one(collection_data)

    def get_collections(self) -> list:
        return self.db.list_collection_names()

    def get_collection_data(self, collection_name: str) -> list:

        collection_lsit = []
        for doc in self.db[collection_name].find():
            collection_lsit.append(doc)

        return collection_lsit
    
    def remove_all_collections(self):
        
        collections = self.db.list_collection_names()
        # Usunięcie każdej kolekcji
        for collection_name in collections:
            self.db[collection_name].drop()


if __name__ == "__main__":
    print("To jest plik klasy MongoUploader. Uruchom proszę skrypt create_mongodb_from_json.")
