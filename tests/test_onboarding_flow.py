import json
import os
import uuid

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from pages.landing_page import LandingPage
from pages.onboarding_flow import Flow, SleepioSignup, FlowStep, DobFlowStep
from pages.report import Report
from utils.driver import DriverFactory
from utils.webdriver_helpers import (
    get_local_storage,
    click_element,
    element_is_active,
    wait_for_element,
    DEFAULT_TIMEOUT,
)


class TestOnboardingFlow:
    @pytest.fixture(scope="function", autouse=True)
    def driver_fixture(self):
        browser = os.getenv("BROWSER")  # get from environment var
        # Since all the tests are browser based, instantiate the driver per test and tear it down
        self.driver = DriverFactory(browser=browser).create_driver()
        yield
        self.driver.close()

    def test_validate_initial_landing_page(self):
        # validates initial presentation of the landing page
        LandingPage(self.driver).open()
        assert LandingPage(self.driver).is_fully_present()

    def test_complete_flow(self):
        # Go through the entire flow and validate each page along the way
        LandingPage(self.driver).open()
        LandingPage(self.driver).get_started()

        for i in range(len(Flow.STEPS)):
            step = Flow.STEPS[i]
            flow_step = FlowStep(
                self.driver, step.name, step.input_type, step.page_number
            )
            assert Flow(self.driver).flow_step_name == flow_step.name
            assert self.driver.current_url == flow_step.expected_url()

            if step.name == "date_of_birth":
                DobFlowStep(self.driver).complete()
            else:
                flow_step.complete()

            # Validate answers are recorded in localStorage
            local_storage = get_local_storage(self.driver)
            answers = json.loads(local_storage.get("sl-answers"))
            answer_dictionary = answers["1"][f"{flow_step.page_number - 1}"][0]
            assert answer_dictionary.get("semantic_id") == flow_step.name
            # TODO assert the values themselves or anything else we want from localStorage
            # TODO we could use selenium wires to inspect the network activity from the browser to validate api/serivce_method_proxy/RecordingAPI/2/post_events and /api/service_method_proxy/Answer/1/create_update_answers_bulk

        # In theory, we should arrive at the Sleepio Signup Step
        SleepioSignup(self.driver).complete(
            first_name="Firsty",
            last_name="Lasty",
            email=f"myemail{str(uuid.uuid4())[:8]}@gmail.com",  # Some randomization
            password="test1234$$B",
        )

        Report(self.driver).wait_for_page_present()
        local_storage = get_local_storage(self.driver)
        for report_key in local_storage.keys():
            if report_key.startswith("sent-report"):
                report_sent = local_storage.get(
                    report_key
                )  # This is int probably generated
                assert report_sent == "true"
                break

    def test_resume_flow(self):
        LandingPage(self.driver).open()
        LandingPage(self.driver).get_started()

        FlowStep(self.driver, "improve_sleep", "checkbox", 1).complete(checkbox_value=1)
        last_step = Flow(self.driver).data_step
        last_flow_step_name = Flow(self.driver).flow_step_name

        # Navigate away
        self.driver.get("https://news.ycombinator.com/")

        # Navigate back
        LandingPage(self.driver).open()
        assert last_step == Flow(self.driver).data_step
        assert last_flow_step_name == Flow(self.driver).flow_step_name

    def test_continue_inactive_until_step_completes(self):
        LandingPage(self.driver).open()
        LandingPage(self.driver).get_started()

        click_element(self.driver, Flow.ELEMENTS["continue_button"])
        assert wait_for_element(self.driver, FlowStep.ELEMENTS["error"])

        # Now complete the form and continue
        FlowStep(self.driver, "improve_sleep", "checkbox", 1).complete(checkbox_value=3)
        assert Flow(self.driver).flow_step_name != "improve_sleep"

    @pytest.mark.parametrize("step", Flow.STEPS, ids=[x.name for x in Flow.STEPS])
    def test_individual_steps(self, step):
        LandingPage(self.driver).open()
        LandingPage(self.driver).get_started()

        # Force URL to a particular step
        flow_step = FlowStep(self.driver, step.name, step.input_type, step.page_number)
        self.driver.get(flow_step.expected_url())

        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda x: Flow(self.driver).flow_step_name == step.name
        )

        if step.name not in ["date_of_birth", "hours_missed"]:
            assert (
                flow_step.get_responses()
            )  # We could enhance this to assert the responses match a known set
