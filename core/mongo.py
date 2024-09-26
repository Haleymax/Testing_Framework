import pymongo


class MongoClint:
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self, url):
        """
        连接到 MongoDB 数据库。

        参数：
        url (str): MongoDB 连接字符串。

        抛出：
        pymongo.errors.ConnectionFailure: 如果连接失败则抛出此异常。
        """
        try:
            self.client = pymongo.MongoClient(url)
        except pymongo.errors.ConnectionFailure as e:
            raise e

    def use_database(self, database):
        """
        选择要使用的数据库。

        参数：
        database (str): 数据库名称。
        """
        self.db = self.client[database]

    def insert_document(self, collection_name, document):
        """
        插入一个文档到指定的集合中。

        参数：
        collection_name (str): 集合名称。
        document (dict): 要插入的文档。

        返回：
        pymongo.collection.Collection: 集合对象。
        """
        if not isinstance(document, dict):
            raise ValueError("document must be a dictionary")
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def find_collection(self, collection_name):
        """
        查找指定集合中的所有文档。

        参数：
        collection_name (str): 集合名称。

        返回：
        list: 包含集合中所有文档的列表。
        """
        collection = self.db[collection_name]
        return list(collection.find())

    def find_date_of_key(self, collection_name, key):
        """
        查找指定集合中包含特定键的第一个文档。

        参数：
        collection_name (str): 集合名称。
        key (str): 要查找的键。

        返回：
        dict or None: 包含特定键的文档，如果没有找到则返回 None。
        """
        collection = self.db[collection_name]
        return collection.find_one({key: {"$exists": True}})

    def update_document(self, collection_name, query, update_data):
        """
        更新指定集合中的一个文档。

        参数：
        collection_name (str): 集合名称。
        query (dict): 用于定位要更新的文档的查询条件。
        update_data (dict): 要应用的更新数据。

        返回：
        pymongo.results.UpdateResult: 更新操作的结果对象。
        """
        if not isinstance(query, dict) or not isinstance(update_data, dict):
            raise ValueError("query and update_data must be dictionaries")
        collection = self.db[collection_name]
        return collection.update_one(query, update_data)

    def delete_document(self, collection_name, query):
        """
        删除指定集合中的一个文档。

        参数：
        collection_name (str): 集合名称。
        query (dict): 用于定位要删除的文档的查询条件。

        返回：
        pymongo.results.DeleteResult: 删除操作的结果对象。
        """
        if not isinstance(query, dict):
            raise ValueError("query must be a dictionary")
        collection = self.db[collection_name]
        return collection.delete_one(query)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()