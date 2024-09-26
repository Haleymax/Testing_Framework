import pymongo

class MongoClint:
    def __init__(self):
        self.db = None

    def connect(self, url, database):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[database]

    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection

    def find_document(self, collection_name, key):
        collection = self.db[collection_name]
        return collection.find(key)

    def update_document(self, collection_name, query, update_data):
        collection = self.db[collection_name]
        return collection.update_one(query, update_data)

    def delete_document(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.delete_one(query)