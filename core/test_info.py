import os
from math import gamma

import pytest

from core.read_data import read_data

from core.all_path import dataPath
from testcases.test_webghost.conftest import webgl_host_data


class TestInfo :
    def __init__(self):
        self.serial = ""
        self.package = ""
        self.type = ""
        self.testtype = ""
        self.gamelist =[]

    def setbaseInfo(self , serialID, packageName, type, testtype):
        self.serial = serialID
        self.package = packageName
        self.type = type
        self.testtype = testtype

    def setgameList(self , gamelist):
        self.gamelist = gamelist

    def creat_dict(self):
        testList = {
            "serial" : self.serial,
            "packageName" : self.package,
            "type" : self.type,
            "testtype" : self.testtype,
            "gamelist" : self.gamelist
        }
        return testList

    def creat_testlist(self):
        testlist = []
        testinfo = []
        testlist.append(self.serial)
        testinfo.append(self.package)
        testinfo.append(self.type)
        testinfo.append(self.testtype)
        for game in self.gamelist :
            lineinfo = testinfo[:]
            lineinfo.append(game)
            testlist.append(lineinfo)
        return testlist


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(dataPath, yaml_file_name)
        yaml_data = read_data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data



def Object_testInfo():
    data = get_data("webgl_host_game_test.yml")
    ObjectList = []
    devices = data["devices"]
    baseinfo = data["package_and_type"][0]
    gameList = data["gamelist"]
    packageName = baseinfo[0]
    type = baseinfo[1]
    testType = baseinfo[2]

    for device in devices :
        infoObject = TestInfo()
        infoObject.setbaseInfo(device[0], packageName, type,testType)
        infoObject.setgameList(gameList)
        ObjectList.append(infoObject)
    return ObjectList





