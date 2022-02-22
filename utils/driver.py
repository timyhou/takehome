from selenium import webdriver


class DriverFactory:
    def __init__(self, browser: str, options=None):
        self.browser = browser
        self.options = options

    def create_driver(self) -> webdriver:
        if self.browser.lower() == "chrome":
            return webdriver.Chrome()
        # TODO - add more browsers and allow for options being passed in
        else:
            raise DriverFactoryError(
                f"Unable to instantiate driver with specified browser {self.browser}"
            )


class DriverFactoryError(Exception):
    pass
