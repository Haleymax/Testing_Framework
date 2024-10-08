import random

from core.get_data import get_data_by_yaml, read_config
from core.logger import logger
from core.mongo import Table, MongoClint


class GamesInfo :
    def __init__(self):
        self.serial = None
        self.package = None
        self.type = None
        self.testtype = None
        self.games = None
        self.gamelist = None

    def set_info(self, serial, package_name, type, test_type, games):
        self.serial = serial
        self.package = package_name
        self.type = type
        self.testtype = test_type
        self.games = games

    def creat_dict(self):
        testlist = {
            "packageName" : self.package,
            "type" : self.type,
            "testtype" : self.testtype,
            "gamelist" : self.games
        }
        return testlist

    def creat_testcase(self):
        testlist = []
        oneinfo = []
        oneinfo.append(self.serial)
        oneinfo.append(self.package)
        oneinfo.append(self.type)
        oneinfo.append(self.testtype)
        for game in self.games :
            current = oneinfo[:]
            current.extend(game)
            testlist.append(current)
        self.gamelist = testlist

    def create_data_for_yal(self, serial):
        data = get_data_by_yaml("webgl_host_game_test.yml")
        base_info = data["package_and_type"][0]
        self.set_info(serial, base_info[0], base_info[1], base_info[2], data["gamelist"])
        logger.info("successfully read the yal file")


    def create_data_for_mongo(self,serial):
        client = MongoClint(read_config.get_mongourl(), read_config.get_database())
        data = client.find_collection(read_config.get_games_collection(), read_config.get_game_table_id())
        self.set_info(serial, data["packageName"], data["type"], data["testtype"], data["gamelist"])
        logger.info("successfully read the mongoDB")

    def get_testcase_by_num(self, num):
        result = self.gamelist[:]
        random.shuffle(result)
        if num != "all" :
            num = int(num)
            if num > len(self.gamelist) or num < 0:
                logger.warning("the input length is too long")
            else:
                result = result[:num]
                logger.info("successfully slice test list")
        logger.info("successfully create test gamelist")
        return result

    def get_testcase_by_order(self, start, end):
        if start > end or start < 0 or end < 0 or end > len(self.gamelist):
            return None
        else:
            result = self.gamelist[start:end]
            return result


def create_gamelist_by_casenum(serial, casenum):
    """
    通过终端输入的 casenum 来创建列表，读取数据的方式在配置文件中设置，分别为 yml 和 mongo
    """
    game_info = GamesInfo()
    if read_config.get_data_function() == "yml":
        game_info.create_data_for_yal(serial)
    elif read_config.get_data_function() == "mongo":
        game_info.create_data_for_mongo(serial)
    else:
        logger.warning("Please set the corrent way to read data")
    game_info.creat_testcase()
    logger.info("successfully create the gamelist")
    return game_info.get_testcase_by_num(casenum)



