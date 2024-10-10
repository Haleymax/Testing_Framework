import time

import requests

from core.games_info import GamesInfo
from core.get_data import read_config
from core.logger import logger
from core.mongo import Table, MongoClint


class Feishu_request:
    def __init__(self, spreadsheetToken, sheetId, access_token):
        self.url = f'https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheetToken}/values/{sheetId}!{self.get_data_range()}'
        logger.info(self.url)
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    def get_data_range(self):
        start_column = read_config.get_start_column()
        total_column = int(read_config.get_total_column())
        start_code = ord(start_column)
        end_code = start_code + total_column
        end_column = chr(end_code)
        range = str(start_column)+str(read_config.get_start_row())+":"+str(end_column)+str(read_config.get_total_row())
        return range

    def get_data_form_feishu(self):
        logger.info("start request data form feishu api")
        data = {}
        retries = 4
        delay = 2
        for attempt in range(0, retries):
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
            else:
                logger.warning(f"attempt {attempt} request failed")
                if attempt < retries - 1:
                    time.sleep(delay)
        return data

    def create_games_data(self):
        request_data = self.get_data_form_feishu()
        game_data = request_data['data']['valueRange']['values'][1:]
        games = []
        for data in game_data:
            game = []
            if data[0] is None or data[3] is None or data[4][0]['type'] != 'url':
                continue
            game.append(data[3])
            game.append(data[4][0]['text'])
            game.append(data[0])
            games.append(game)
        return games

    def insert_mongo(self):
        feishu_data = self.create_games_data()
        insert = GamesInfo()
        insert.set_info("", "com.u3d.webglhost", "unity 引擎小游戏", "compatibility", feishu_data)
        insert_data = insert.creat_dict()
        return insert_data



def updata_feishu_data_for_mongo():
    data_of_feishu = Feishu_request(read_config.get_spreadsheetToken(),read_config.get_sheetId(),read_config.get_access_token())
    data = data_of_feishu.insert_mongo()
    insert_table = Table(read_config.get_game_table_id(), data)
    mongo_client = MongoClint(read_config.get_mongourl(), read_config.get_database())
    mongo_client.insert_document(read_config.get_games_collection(), insert_table)


if __name__ == '__main__':
    updata_feishu_data_for_mongo()