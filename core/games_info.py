import random

from core.get_data import get_data_by_yaml, read_config
from core.logger import logger
from core.mongo import Table, MongoClint

read_config

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
        data = client.find_collection(read_config.get_collection(), read_config.get_game_table_id())
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



def create_gamelist_by_casenum(serial, casenum):
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


def update():
    logger.info("start update mongodb database")
    game_info = GamesInfo()
    game_info.create_data_for_yal("")
    game_info.creat_testcase()
    new_data = game_info.creat_dict()
    objectData = Table(read_config.get_game_table_id(), new_data)
    client = MongoClint(read_config.get_mongourl(), read_config.get_database())
    client.insert_document(read_config.get_database(), read_config.get_collection(), objectData)



if __name__ == '__main__':
    update()

