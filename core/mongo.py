import pymongo


class MongoClint:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self, url):
        try:
            self.client = pymongo.MongoClient(url)
        except pymongo.errors.ConnectionFailure as e:
            raise e

    def use_database(self, database):
        self.db = self.client[database]

    def insert_document(self, collection_name, document):
        if not isinstance(document, dict):
            raise ValueError("document must be a dictionary")
        collection = self.db[collection_name]
        return collection.insert(document)

    def find_collection_one(self,collection_name):
        collection = self.db[collection_name]
        return collection.find_one()
    def find_collection(self, collection_name):
        collection = self.db[collection_name]
        data = collection.find()
        return data

    def update_document(self, collection_name, query, update_data):
        if not isinstance(query, dict) or not isinstance(update_data, dict):
            raise ValueError("query and update_data must be dictionaries")
        collection = self.db[collection_name]
        return collection.update_one(query, update_data)

    def delete_document(self, collection_name, query):
        if not isinstance(query, dict):
            raise ValueError("query must be a dictionary")
        collection = self.db[collection_name]
        return collection.delete_one(query)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()