import os
import pytest
from core.read_data import read_data
from core.all_path import dataPath


class TestInfo :
    def __init__(self):
        self.package = ""
        self.type = ""
        self.testtype = ""
        self.gamelist =[]

    def set_base_info(self, serialid, package_name, type, test_type):
        self.serial = serialid
        self.package = package_name
        self.type = type
        self.testtype = test_type

    def set_game_list(self, gamelist):
        self.gamelist = gamelist

    def creat_dict(self):
        testlist = {
            "packageName" : self.package,
            "type" : self.type,
            "testtype" : self.testtype,
            "gamelist" : self.gamelist
        }
        return testlist

    def creat_testlist(self):
        testlist = []
        testinfo = []
        testinfo.append(self.serial)
        testinfo.append(self.package)
        testinfo.append(self.type)
        testinfo.append(self.testtype)
        for game in self.gamelist :
            current = testinfo[:]
            current.extend(game)
            testlist.append(current)
        return testlist


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(dataPath, yaml_file_name)
        yaml_data = read_data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data







