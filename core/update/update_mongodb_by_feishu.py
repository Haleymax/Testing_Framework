from core.feishu import Feishu_request
from core.get_data import read_config
from core.mongo import Table, MongoClint


def updata_feishu_data_for_mongo():
    data_of_feishu = Feishu_request(read_config.get_spreadsheetToken(),read_config.get_sheetId(),read_config.get_access_token())
    data = data_of_feishu.insert_mongo()
    insert_table = Table(read_config.get_game_table_id(), data)
    mongo_client = MongoClint(read_config.get_mongourl(), read_config.get_database())
    mongo_client.insert_document(read_config.get_games_collection(), insert_table)


if __name__ == '__main__':
    updata_feishu_data_for_mongo()