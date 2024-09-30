import pymongo


from core.logger import logger

class GameList:
    def __init__(self):
        self.game_list = []


    def set_gamelist(self, games):
        self.game_list = games

    def compare(self, otherList):
        """
        这个方法用于MongoDB中存储的游戏列表和从yaml中读取的游戏列表进行比较
        :param otherList: yaml文件中读取到的游戏列表
        :return: 若是一样就返回True ， 存在差异就返回False
        """
        if len(self.game_list) != len(otherList) :
            return False
        for list1 , list2 in zip(self.game_list, otherList):
            if len(list1) != len(list2):
                return False
            for element1 , element2 in zip(list1, list2):
                if element1 != element2:
                    return False
        return True

class MongoClint:
    def __init__(self):
        self.client = None
        self.db = None
        self.id = ""

    def connect(self, url):
        try:
            self.client = pymongo.MongoClient(url)
            logger.info(f"Successful established a connection with the mongodb server")
        except pymongo.errors.ConnectionFailure as e:
            logger.info(f"Failed to establish connection with the mongodb server")
            raise e

    def set_id(self, id):
        self.id = id

    def use_database(self, database):
        self.db = self.client[database]

    def insert_document(self, collection_name, document):
        if not isinstance(document, dict):
            logger.info("error in data transfer,need dictionary")
            return None
        collection = self.db[collection_name]
        logger.info(f"successfully added {document} to {collection_name}")
        return collection.insert_one(document)

    def find_collection_one(self,collection_name):
        collection = self.db[collection_name]
        logger.info("successfully queried a piece of data")
        return collection.find_one()


    def find_collection(self, collection_name):
        collection = self.db[collection_name]
        data = collection.find()
        logger.info("successfully queried a dictortion")
        return data

    def find_value_by_key(self,key):
        result = self.db.find_one({key : {"$exists" : True}})
        if result :
            return result.get("key")
        else:
            return None

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

    def insert_gamelist(self, collection_name , Object):
        """
        插入游戏列表
        :param collection_name:
        :param Object:
        :return:
        """
        gametest_dict = Object.creat_dict()
        self.insert_document(collection_name,gametest_dict)