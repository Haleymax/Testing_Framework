import pytest

from core import read_data
from core.all_path import appPath, config_file_path
from core.file_download import Request, isExist, clear_file, download_resources, unzip_file
from core.logger import logger
from core.read_data import ReadFileDate


def get_mongourl():
    logger.info("读取 mogo 连接地址")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    properties = read.load_properties(config_file_path)["properties"]
    return properties['mongourl']

def get_database():
    logger.info("读取 database")
    read = ReadFileDate()
    # test = read.load_ini(config_file_path)
    properties = read.load_properties(config_file_path)["properties"]
    return properties['database']

def get_devices():
    logger.info("读取 collection")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    properties = read.load_properties(config_file_path)["properties"]
    return properties['devices']

def get_games():
    logger.info("读取 collection")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    properties = read.load_properties(config_file_path)["properties"]
    return properties["gamelist"]