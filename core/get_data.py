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
        read_data.load_ini(config_file_path)

    def get_mongourl(self):
        logger.info("读取 mogo 连接地址")
        properties = read_data.load_properties(config_file_path)["mongoDB"]
        return properties['mongourl']

    def get_database(self):
        logger.info("读取 database")
        properties = read_data.load_properties(config_file_path)["mongoDB"]
        return properties['database']

    def get_collection(self):
        logger.info("读取 collection")
        read_data.load_ini(config_file_path)
        properties = read_data.load_properties(config_file_path)["mongoDB"]
        return properties["collection"]

    def get_game_table_id(self):
        logger.info("读取 游戏字段id")
        properties = read_data.load_properties(config_file_path)["mongoDB"]
        return properties["games_id"]

    def get_device_table_id(self):
        logger.info("读取 设备字段id")
        properties = read_data.load_properties(config_file_path)["mongoDB"]
        return properties["device_table_id"]

    def get_data_function(self):
        logger.info("获取数据库的类型")
        properties = read_data.load_properties(config_file_path)["data"]
        return properties["function"]

read_config = ReadConfig()