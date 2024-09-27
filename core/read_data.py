from configparser import ConfigParser
from distutils.command.config import config
from idlelib.iomenu import encoding

import yaml

from core.logger import logger


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 和 .properties 文件的 键 option 自动转为小写的问题
    def __init__(self , defaults = None):
        ConfigParser.__init__(self, defaults = defaults)
    def optionxform(self, optionstr):
        return optionstr

class ReadFileDate :

    def __init__(self):
        pass

    def load_yaml(self , file_path):
        logger.info("加载 {} 文件......".format(file_path))
        with open(file_path , encoding='utf-8') as f :
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data


    def load_properties(self , file_path):
        logger.info(f"加载 {file_path} 文件......")
        config = MyConfigParser()
        config.read(file_path,encoding = "UTF-8")
        data = dict(config._sections)
        logger.info(f"读到数据 ==>> {data}")
        return data