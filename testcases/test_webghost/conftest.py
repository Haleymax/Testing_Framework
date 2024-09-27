import pytest

from core import read_data
from core.all_path import config_file_path
from core.logger import logger
from core.mongo import MongoClint
from core.read_data import ReadFileDate


@pytest.fixture(scope="session")
def get_mongourl():
    logger.info("读取 mogo 连接地址")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    mogourl = read.load_properties(config_file_path)["mongourl"]
    return mogourl


@pytest.fixture(scope="session")
def get_database():
    logger.info("读取 database")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    database = read.load_properties(config_file_path)["database"]
    return database


@pytest.fixture(scope="session")
def get_collection():
    logger.info("读取 collection")
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    collection = read.load_properties(config_file_path)["collection"]
    return collection


def get_data(get_mongourl, get_database, get_collection):
    client = MongoClint()
    mogourl = get_mongourl
    database = get_database
    collection = get_collection
    client.connect(mogourl)
    client.use_database(database)
    data = client.find_collection(collection)
    result = []
    webgl_host_data = {}
    for x in data:
        linedata = []
        deviceid = x['deviceid']
        packagename = x['packagename']
        typename = x['type']
        gamelist = x['gamelist']
        linedata.append(deviceid)
        linedata.append(packagename)
        linedata.append(typename)
        for key, value in gamelist.items():
            line2 = linedata[:]
            line2.append(str(key))
            line2.append(str(value))
            result.append(line2)
        webgl_host_data['test_webgl_host'] = result
    return webgl_host_data



webgl_host_data = get_data(get_mongourl, get_database, get_collection)