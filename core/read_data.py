import yaml

from core.logger import logger


class ReadFileDate :

    def __init__(self):
        pass

    def load_yaml(self , file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path , encoding='utf-8') as f :
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data