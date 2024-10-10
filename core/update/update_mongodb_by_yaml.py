from core.games_info import GamesInfo
from core.get_data import read_config
from core.logger import logger
from core.mongo import Table, MongoClint


def update_mangodb_by_yaml():
    logger.info("start update mongodb database")
    game_info = GamesInfo()
    game_info.create_data_for_yal("")
    game_info.creat_testcase()
    new_data = game_info.creat_dict()
    insert_data = Table(read_config.get_game_table_id(), new_data)
    client = MongoClint(read_config.get_mongourl(), read_config.get_database())
    client.insert_document(read_config.get_games_collection(), insert_data)



if __name__ == '__main__':

    update_mangodb_by_yaml()