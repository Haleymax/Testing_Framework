import os
import random
import shutil
import time
import zipfile

import requests

from core.all_path import appPath, base_path
from core.get_data import read_config
from core.logger import logger
from core.mongo import Table, MongoClint

read_config

class PipJobInfo:
    def __init__(self, id):
        self.id = id
        self.data = {}

    def add_data(self, data):
        self.data[str(data["id"])] = data

    def get_data(self):
        return self.data

class Getlab_request:
    def __init__(self, private_token):
        self.url = None
        self.headers = {'PRIVATE-TOKEN' : private_token}

    def set_url_by_jobid(self, job_id):
        self.url = "https://gitlab-fw.internal.unity.cn/api/v4/projects/348/jobs/"+str(job_id)+"/artifacts"

    def set_url_by_pipeline_id(self, pipeline_id):
        self.url = "https://gitlab-fw.internal.unity.cn/api/v4/projects/348/pipelines/"+str(pipeline_id)+"/jobs"

    def show_info(self):
        logger.info(self.url)
        logger.info(self.headers)

    def download_resources(self):
        logger.info("execute download file...")
        retries = 4
        delay = 2
        for attempt in range(retries):
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                try:
                    random_number = random.randint(1000, 9999)
                    zip_filename = f'app_host_{random_number}.zip'
                    zippath = os.path.join(appPath, zip_filename)
                    with open(zippath, 'wb') as zf:
                        zf.write(response.content)
                        logger.info("successfully write compressed package")
                except Exception as e:
                    logger.warning("Fail to write compressed package")
                break
            else:
                logger.warning(f"attempt {attempt + 1} request failed")
                if attempt < retries - 1:
                    time.sleep(delay)

    def download_by_pipeline_id(self, pipeline_id):
        """
        通过pipeline_id去下载资源
        """
        self.set_url_by_pipeline_id(pipeline_id)
        data = self.get_pipeinfo_by_mongo(pipeline_id)
        for job_id in data:
            self.set_url_by_jobid(job_id)
            self.download_resources()

    def get_pipeinfo_by_mongo(self, pipeline_id):
        """
        通过pipeline_id在mongo中获取信息，如果没有查找到就通过请求gatlab拉取到信息再将这个信息插入到数据库中
        """
        mongo = MongoClint(read_config.get_mongourl(), read_config.get_database())
        data = mongo.find_collection(read_config.get_pipecollection(),pipeline_id)
        if data == None:
            data = self.get_pipeinfo_by_gatlab(pipeline_id).data
            self.inser_mongo(pipeline_id)
        job_ids = []
        for job_id in data.keys():
            if job_id == "_id":
                continue
            job_ids.append(job_id)
        return job_ids

    def get_pipeinfo_by_gatlab(self, pipeline_id):
        """
        通过pipeline_id获取到对应的请求数据，数据中对应的就是job的详细信息
        """
        self.set_url_by_pipeline_id(pipeline_id)
        pipeinfo = PipJobInfo(pipeline_id)
        logger.info("execute get pipline info...")
        retries = 4
        delay = 2
        for attempt in range(retries):
            response = requests.get(self.url, headers=self.headers)
            if response.status_code == 200:
                try:
                    datas = response.json()
                    for data in datas:
                        pipeinfo.add_data(data)
                    logger.info("successfully get pipline info by gatlab")
                except Exception as e:
                    logger.warning(f"Fail to get pipline info")
                break
            else:
                logger.warning(f"attempt {attempt + 1} request failed")
                if attempt < retries - 1:
                    time.sleep(delay)
        return pipeinfo

    def inser_mongo(self, pipeline_id):
        """
        将获取到的数据插入到pipeline的集合中，其中集合中数据的键为pipeline的id，集合中的每个子集合的键就是jobid
        """
        logger.info("Insert data of pipeline into mongodb...")
        pipinfo = self.get_pipeinfo_by_gatlab(pipeline_id)
        inser_data = Table(pipinfo.id, pipinfo.data)
        mongo = MongoClint(read_config.get_mongourl(), read_config.get_database())
        mongo.insert_document(read_config.get_pipecollection(), inser_data)

def is_exist(dirPath):
    pathExist = os.path.isdir(dirPath)
    if pathExist :
        logger.info(f"{dirPath} file exists")
    else:
        os.makedirs(dirPath,0o777)
        logger.info("dir does not exist but has been created")


def clear_file(dir_path) :
    logger.info("execute clear file...")
    files = os.listdir(dir_path)
    if not files:
        logger.info("file is empty and no need to execute")
        return
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    logger.info("file clearing completed")


def unzip_file(file_path):
    logger.info("execute decompressed file...")
    files = os.listdir(file_path)
    if not files:
        logger.info("file is empty and no need to execute")
        return
    try:
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(file_path, file)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(file_path)
        logger.info("successfully decompressed file")
    except Exception as e:
        logger.info("File decompression failed")