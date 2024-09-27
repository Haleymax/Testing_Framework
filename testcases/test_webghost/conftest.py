import pytest

from core import read_data
from core.all_path import config_file_path
from core.mongo import MongoClint
from core.read_data import ReadFileDate


@pytest.fixture(scope="session")
def get_mongourl():
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    mogourl = read.load_properties(config_file_path)["mongourl"]
    return mogourl

@pytest.fixture(scope="session")
def get_database():
    read = ReadFileDate()
    test = read.load_ini(config_file_path)
    database = read.load_properties(config_file_path)["database"]
    return database

@pytest.fixture(scope="session")
def get_collection():
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


