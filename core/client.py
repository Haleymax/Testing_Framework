import time

from retry import retry
from yaml import NodeEvent
import uiautomator2 as u2

from core.logger import logger


class Client :

    def __init__(self,serial):
        self.serial = serial
        self.driver = None

    def connect_with_retry(self):
        retries = 5
        delay = 5

        for attempt in range(retries) :
            try:
                self.driver = u2.connect(self.serial)
                logger.info(self.driver.info)
                logger.info(f"Successfully connect to device: {self.serial}")
                return
            except Exception as e:
                logger.info(f"Attempt {attempt + 1} failed:{e}")

            if attempt < retries - 1 :
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        raise Exception(f"Failed to connect to device after {retries} attempts")

    def get_driver(self):
        return self.driver

    def start_app(self , packname):
        self.driver.app_start(packname)

    def stop_app(self , packname):
        self.driver.app_stop(packname)

    def send_text(self , locator , value):
        self.ge