import time

from Tools.scripts.make_ctype import method
from retry import retry
from scripts.regsetup import description
from yaml import NodeEvent
import uiautomator2 as u2

from core.logger import logger

class By:
    Text = "text"
    ResourceId = "resourceId"
    Description = "description"
    ClassName = "className"

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

    def get_elem(self , locator):
        method , l = locator

        if method == By.Text:
            if self.driver(text=l).exists:
                return self.driver(text=l)
        if method == By.ResourceId:
            if self.driver(resourceId=l).exists:
                return self.driver(resourceId=l)
        if method == By.Description:
            if self.driver(description=l).exists:
                return self.driver(description=l)
        if method == By.ClassName:
            if self.driver(class_name=l).exists:
                return self.driver(class_name=l)
        return None

def click(self , locator) :
    retries = 3
    delay = 2
    for attempt in range(3):
        element = self.get_elem(locator)
        if element is not None:
            element.click()
            return
        else:
            logger.info(f"Attempt {attempt + 1} failed")
            if attempt < retries-1:
                time.sleep(delay)
    raise Exception(f"{logger} not found")


    def send_text(self , locator , value):
        self.get_elem(locator).set_text(value)