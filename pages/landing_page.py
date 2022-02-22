from pages.base_component import BaseComponent, Openable
from utils.webdriver_helpers import (
    type_in_element,
    get_element,
    click_element,
    wait_for_element_attribute,
)


class LandingPage(Openable, BaseComponent):
    BASE_URL = "https://onboarding.sleepio.com/sleepio/big-health"
    # map container name of the elements and their css selector
    ELEMENTS = {
        "app_container": "#sl-flow",
        "header": "header.sl-header",
        "footer": "#footer-wrapper",
        "login_button": "a.sl-header__login",
        "landing_page_button": "div.landing-page button",
        "contact_us_button": "#transparent-button",
    }

    def get_started(self):
        click_element(self.driver, self.ELEMENTS.get("landing_page_button"))
        assert wait_for_element_attribute(
            self.driver,
            self.ELEMENTS.get("app_container"),
            "data-step",
            "1",
        )


# Wasn't sure if this was in scope
class ContactUsIframe(BaseComponent):
    ELEMENTS = {
        "iframe": "#designstudio-iframe",
        "name_input": "",
        "email_input": "",
        "question_input": "",
        "email_us_button": "",
    }

    def enter_input(self, name, email, question):
        # Make sure we switch to iframe
        self.driver.switch_to.frame(
            get_element(self.driver, self.ELEMENTS.get("iframe"))
        )
        type_in_element(self.driver, self.ELEMENTS.get("name_input"), name)
        type_in_element(self.driver, self.ELEMENTS.get("email_input"), email)
        type_in_element(self.driver, self.ELEMENTS.get("question_input"), question)
        get_element(self.driver, self.ELEMENTS.get("email_us_button")).click()
        # and switch out
        self.driver.switch_to_default_content()
