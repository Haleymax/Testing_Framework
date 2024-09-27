from core.mongo import MongoClint


def get_data():
    client = MongoClint()
    url = "mongodb://localhost:27017/"
