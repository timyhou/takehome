from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from pages.base_component import BaseComponent
from pages.landing_page import LandingPage
from utils.webdriver_helpers import (
    get_element,
    click_element,
    wait_for_element_active,
    get_elements,
    type_in_element,
)


class Step:
    """Plain old object that contains the information about a specific step"""

    def __init__(self, name, input_type, page_number, responses: list = None):
        self.name = name
        self.input_type = input_type
        self.page_number = page_number
        self.responses = responses if responses else []


class FlowStep:
    """A webdriver component object that allows interaction with a specific step"""

    ELEMENTS = {
        "select": "select.sl-select",
        "radio": ".sl-options-wrapper input[type=radio]",
        "checkbox": "input[type=checkbox]",
        "response_label": ".sl-option",
        "number": "input[type=number]",
        "error": ".sl-general-error",
    }

    def __init__(self, driver, name, input_type, page_number):
        self.driver = driver
        self.name = name
        self.input_type = input_type
        self.page_number = page_number

    def get_responses(self):
        if self.input_type == "select":
            select = Select(get_element(self.driver, self.ELEMENTS.get("select")))
            options = select.options
            return [x.text for x in options]
        elif self.input_type == "radio":
            radio_buttons = get_elements(
                self.driver, self.ELEMENTS.get("response_label")
            )
            return [x.text for x in radio_buttons]
        elif self.input_type == "checkbox":
            checkboxes = get_elements(self.driver, self.ELEMENTS.get("response_label"))
            return [x.text for x in checkboxes]
        else:
            return []

    def expected_url(self):
        return f"{LandingPage.BASE_URL}#2/{self.page_number}"

    def complete(self, select_value=1, radio_value=1, checkbox_value=1, number_value=1):
        """
        Args:
            number_value: value for a number input field
            select_value: index value of select option to choose
            radio_value: index value of select option to choose
            checkbox_value: index value of select option to choose
        """
        if self.input_type == "select" and select_value:
            select = Select(get_element(self.driver, self.ELEMENTS.get("select")))
            select.select_by_index(select_value)
        elif self.input_type == "radio" and radio_value:
            radio_buttons = get_elements(self.driver, self.ELEMENTS.get("radio"))
            radio_buttons[radio_value].click()
        elif self.input_type == "checkbox" and checkbox_value:
            checkboxes = get_elements(self.driver, self.ELEMENTS.get("checkbox"))
            checkboxes[checkbox_value].click()
        elif self.input_type == "number" and number_value:
            type_in_element(self.driver, self.ELEMENTS.get("number"), number_value)
        else:
            raise Exception(f"Unknown flow step input type {self.input_type}")

        wait_for_element_active(self.driver, Flow.ELEMENTS["continue_button"])
        click_element(self.driver, Flow.ELEMENTS["continue_button"])


class DobFlowStep(BaseComponent):
    ELEMENTS = {"month": "#select-month", "day": "#select-day", "year": "#select-year"}

    def __init__(self, driver: WebDriver):
        self.name = "date_of_birth"
        self.page_number = 11
        super(DobFlowStep, self).__init__(driver)

    def complete(self, month: str = "September", day: str = "20", year: str = "1980"):
        select_month = Select(get_element(self.driver, self.ELEMENTS.get("month")))
        select_month.select_by_value(month)
        select_day = Select(get_element(self.driver, self.ELEMENTS.get("day")))
        select_day.select_by_value(day)
        select_year = Select(get_element(self.driver, self.ELEMENTS.get("year")))
        select_year.select_by_value(year)

        wait_for_element_active(self.driver, Flow.ELEMENTS["continue_button"])
        click_element(self.driver, Flow.ELEMENTS["continue_button"])


class SleepioSignup(BaseComponent):
    ELEMENTS = {
        "first_name": "input[name='first_name']",
        "last_name": "input[name='last_name']",
        "email": "input[name='email']",
        "password": "input[name='password']",
        "checkboxes": "input[type=checkbox]",
    }

    def __init__(self, driver):
        self.name = "new-sleepio-signup-optional-eligibility-v2"
        super(SleepioSignup, self).__init__(driver)

    def complete(self, first_name: str, last_name: str, email: str, password: str):
        # Handle first name, last name, email, password
        type_in_element(self.driver, self.ELEMENTS.get("first_name"), first_name)
        type_in_element(self.driver, self.ELEMENTS.get("last_name"), last_name)
        type_in_element(self.driver, self.ELEMENTS.get("email"), email)
        type_in_element(self.driver, self.ELEMENTS.get("password"), password)

        # Checkboxes for ToS and Acknowledge
        checkboxes = get_elements(self.driver, self.ELEMENTS.get("checkboxes"))
        for box in checkboxes:
            box.click()

        wait_for_element_active(self.driver, Flow.ELEMENTS["continue_button"])
        click_element(self.driver, Flow.ELEMENTS["continue_button"])


class Flow(BaseComponent):
    ELEMENTS = {
        "flow_container": "#sl-flow",
        "flow_step_content": "div[data-semantic-id]",
        "continue_button": "div.sl-page .sl-button-wrapper",
    }

    # Sequence of steps in the overall onboarding flow
    # I realized that there is some branching so this is partially incorrect
    # With the branching a tree like structure would be better suited than a list
    STEPS = [
        Step("improve_sleep", "checkbox", 1),
        Step("problem_sleep", "select", 2),
        Step("stop_sleeping", "radio", 3),
        Step("troubled_in_general", "select", 4),
        Step("problem_nights", "select", 5),
        Step("unable_to_control", "select", 6),
        Step("fall_asleep_stay_awake", "select", 7),
        Step("gender", "radio", 10),
        Step("date_of_birth", None, 11),
        Step("employment_status", "select", 12),
        Step("affect_productivity", "select", 13),
        Step("hours_missed", "number", 14),
        Step("expert_guides", "checkbox", 15),
    ]

    @property
    def data_step(self) -> int:
        e = get_element(self.driver, self.ELEMENTS.get("flow_container"))
        return e.get_attribute("data-step")

    @property
    def flow_step_name(self) -> str:
        e = get_element(self.driver, self.ELEMENTS.get("flow_step_content"))
        return e.get_attribute("data-semantic-id")
