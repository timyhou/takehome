"""
This module is a collection of static helper methods for common webdriver actions
"""
import json
from typing import Optional

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

DEFAULT_TIMEOUT = 10


def element_is_present(driver: WebDriver, css_selector: str) -> bool:
    try:
        driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
        return True
    except NoSuchElementException:
        return False


def element_is_active(driver: WebDriver, css_selector: str) -> bool:
    # Assumes the element exists already so this can raise a NoSuchElementException
    e = driver.find_element(by=By.CSS_SELECTOR, value=css_selector)
    return e.is_enabled()


def element_is_present_and_active(driver: WebDriver, css_selector: str) -> bool:
    return element_is_present(driver, css_selector) and element_is_present(
        driver, css_selector
    )


# For all the gets, types, and clicks, build in automatic waiting
def get_element(driver: WebDriver, css_selector: str) -> Optional[WebElement]:
    try:
        return wait_for_element(driver, css_selector)
    except NoSuchElementException:
        return None


def get_elements(driver: WebDriver, css_selector: str) -> [WebElement]:
    try:
        if wait_for_element(driver, css_selector):
            return driver.find_elements(by=By.CSS_SELECTOR, value=css_selector)
        return None
    except NoSuchElementException:
        return None


def type_in_element(driver: WebDriver, css_selector, text_input):
    e = wait_for_element(driver, css_selector)
    e.send_keys(text_input)


def click_element(driver: WebDriver, css_selector):
    get_element(driver, css_selector).click()


def wait_for_element(
    driver: WebDriver, css_selector: str, timeout: int = DEFAULT_TIMEOUT
) -> WebElement:
    try:
        return WebDriverWait(driver, timeout).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, css_selector)
            )
        )
    except TimeoutException:
        raise NoSuchElementException(
            f"Waited {DEFAULT_TIMEOUT} for element at {css_selector} but was not found!"
        )


def wait_for_element_attribute(
    driver: WebDriver,
    css_selector: str,
    attribute: str,
    value: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            lambda x: get_element(driver, css_selector).get_attribute(attribute)
            == value
        )
        return True
    except TimeoutException:
        return False


def wait_for_element_active(
    driver: WebDriver, css_selector: str, timeout: int = DEFAULT_TIMEOUT
):
    WebDriverWait(driver, timeout).until(
        expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )


def get_local_storage(driver: WebDriver) -> dict:
    return driver.execute_script(
        "var storage = window.localStorage; "
        "var items = {}; "
        "for (var i =0; i < storage.length; i++) {items[storage.key(i)] = storage.getItem(storage.key(i))}; "
        "return items; "
    )
