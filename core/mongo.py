import pymongo


from core.get_data import read_config
from core.logger import logger

class Table:
    """
    这个Table类并不是指一个mongodb中的集合，而是指这个集合下的一条数据
    """
    def __init__(self,id ,data):
        self.data = data
        self.id = id

    def get_table(self):
        return self.data

class MongoClint:
    def __init__(self, url, database):
        try:
            self.client = pymongo.MongoClient(url)
            logger.info(f"Successful established a connection with the mongodb server")
        except Exception as e:
            logger.info(f"Failed to establish connection with the mongodb server")
            raise e
        self.db = self.client[database]

    def insert_document(self, collection_name, table):
        if not isinstance(table.data, dict):
            logger.info("error in data transfer,need dictionary")
            return None
        collection = self.db[collection_name]
        if table.data == {}:
            logger.warning("there is an error in inserting data,please check")
        else:
            # 根据这个表的id插入数据，若id存在覆盖新的数据进入，若id不存在则直接插入数据
            try:
                collection.replace_one({"_id": table.id}, table.data, upsert=True)
                logger.info(f"successfully inserted {collection_name}")
            except Exception as e:
                logger.info(f"Failed to insert ,becaues {e}")

    def find_collection(self, collection_name, id):
        collection = self.db[collection_name]
        data = collection.find_one({"_id":id})
        if data:
            logger.info(f"successfully queried a document from collection '{collection_name}' with id '{id}'.")
        else:
            logger.warning(f"Failed to query a document from collection '{collection_name}' with id '{id}'.")
        return data


    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("disconnect the mongodb server")
        if self.client:
            self.client.close()