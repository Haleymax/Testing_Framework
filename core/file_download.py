import os
import shutil
import time
import zipfile
from importlib.metadata import files

import requests
from yaml import NodeEvent

from core.all_path import appPath, base_path
from core.logger import logger

class Request:
    def __init__(self):
        self.method= None
        self.url = None
        self.headers = {}
        self.data = None

    def set_requset(self, job_id, private_token):
        self.url = url = "https://gitlab-fw.internal.unity.cn/api/v4/projects/348/jobs/"+job_id+"/artifacts"
        self.headers = {'PRIVATE-TOKEN' : private_token}

def isExist(dir):
    pathExist = False
    dirPath = os.path.join(base_path,dir)
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    pathExist = dir in directories
    if pathExist :
        logger.info(f"{dirPath} file exists")
    else:
        os.makedirs(dirPath,0o777)
        logger.info("dir does not exist but has been created")

def clear_file(dir_path) :
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    logger.info("file clearing completed")

def download_resources(request) :
    retries = 4
    delay = 2
    for attempt in range(3):
        response = requests.get(request.url, request.url, headers=request.headers)
        if response.status_code == 200:
            try:
                zip_filename = 'app_host.zip'
                zippath = os.path.join(appPath, zip_filename)
                with open(zippath , 'wb') as zf:
                    zf.write(response.content)
            except Exception as e:
                logger.info("Fail to write compressed package")
            break
        else:
            logger.info(f"attempt {attempt+1} request failed")
            if attempt < retries - 1:
                time.sleep(delay)

def unzip_file(file_path):
    files = os.listdir(file_path)
    try:
        for file in files:
            if file.endswith('.zip'):
                zip_file_path = os.path.join(file_path, file)
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(file_path)
        logger.info("successfully decompressed file")
    except Exception as e:
        logger.info("File decompression failed")