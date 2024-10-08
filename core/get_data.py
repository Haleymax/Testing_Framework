import os

import pymongo
import pytest
from pymongo import MongoClient

from core.all_path import dataPath, config_file_path
from core.logger import logger
from core.read_data import read_data


def get_data_by_yaml(yaml_file_name):
    try:
        data_file_path = os.path.join(dataPath, yaml_file_name)
        yaml_data = read_data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


def get_data_by_mongo(mongourl, database, collection):
    client = MongoClient(mongourl, database)
    data = client.find_collection(collection)
    return data

class ReadConfig:
    def __init__(self):
        self.data = read_data.load_ini(config_file_path)

    def get_mongourl(self):
        logger.info("读取 mogo 连接地址")
        config = self.data["mongoDB"]
        return config['mongourl']

    def get_database(self):
        logger.info("读取 database")
        config = self.data["mongoDB"]
        return config['database']

    def get_games_collection(self):
        logger.info("读取 collection")
        config = self.data["mongoDB"]
        return config["games_collection"]

    def get_pipe_collection(self):
        logger.info("读取 pipe collection")
        config = self.data["mongoDB"]
        return config["pipe_collection"]

    def get_game_table_id(self):
        logger.info("读取 游戏字段id")
        config = self.data["mongoDB"]
        return config["games_id"]

    def get_device_table_id(self):
        logger.info("读取 设备字段id")
        config = self.data["mongoDB"]
        return config["device_table_id"]

    def get_data_function(self):
        logger.info("获取数据库的类型")
        config = self.data["data"]
        return config["function"]

    def get_spreadsheetToken(self):
        logger.info("获取飞书表格的token")
        properties = self.data["feishu"]
        return properties["spreadsheetToken"]

    def get_sheetId(self):
        logger.info("获取表格子表id")
        properties = self.data["feishu"]
        return properties["sheetId"]

    def get_access_token(self):
        logger.info("获取连接token")
        properties = self.data["feishu"]
        return properties["access_token"]

    def get_start_row(self):
        logger.info("获取起始点行坐标")
        properties = self.data["feishu"]
        return properties["start_row"]

    def get_start_column(self):
        logger.info("获取起始点列坐标")
        properties = self.data["feishu"]
        return properties["start_column"]

    def get_total_row(self):
        logger.info("获取数据的总行数")
        properties = self.data["feishu"]
        return properties["total_row"]

    def get_total_column(self):
        logger.info("获取数据的总列数")
        properties = self.data["feishu"]
        return properties["total_column"]

read_config = ReadConfig()
read_config = ReadConfig()