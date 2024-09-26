import pymongo

class MongoClint:
    def __init__(self):
        self.db = None

    def connect(self, url, database):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[database]



