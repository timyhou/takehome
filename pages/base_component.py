import logging

import furl
from selenium.webdriver.remote.webdriver import WebDriver

from utils.webdriver_helpers import element_is_present, wait_for_element


# All UI widgets or pages shall inherit from here
class BaseComponent:
    ELEMENTS = {}

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_page_present(self):
        for element_name, locator in self.ELEMENTS.items():
            wait_for_element(self.driver, locator)

    def is_fully_present(self) -> bool:
        missing = {}
        for element_name, locator in self.ELEMENTS.items():
            if not element_is_present(self.driver, locator):
                logging.error(
                    f"The following element {element_name} was not located on page {self.driver.current_url} with {locator} "
                )
                missing[element_name] = locator
        return False if missing else True


# Represents a page that is directly openable via a URL
class Openable:
    BASE_URL = ""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Tell webdriver to open a page and add any additional url parameters to the URL
    def open(self, **kwargs):
        furled = furl.furl(self.BASE_URL).add(args=kwargs).url
        self.driver.get(furled)
