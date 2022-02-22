## Instructions & requirements
1. This project depends on python 3.9.x
   1. Setup a virtualenv using your preferred method
2. Install dependencies`pip install requirements.txt`
3. Ensure you have at least chromedriver installed and setup
4. Execute tests with `pytest` 

## Test Strategy

Sleepio onboarding experience

- Landing page
  - Verify Presentation
    - Given a first time user when they open the page
      - Key elements are present
        - SPA app is mounted
        - Log in button present and active
        - Header & footer content present
        - Contact Us Iframe present and active (but minimized)
    - Given a returning user when they open the page: 
      - Should return to the last "viewed" flow step
      - This is persisted by browser localStorage: 
        - sl-answers
        - sl-flow-max-progress
        - sl-flow-progress
        - times-to-show
  - Verify landing page functionality
    - Given a user on the landing page when they:
      - Click on Get Started the onboarding flow with the first question
          - `<div id=sl-flow>` has attribute `data-step` increment by 1 
          - First question content is rendered under `<div class="s1-page"> <div data-semantic-id="stage name">`
      - Click the Log in button redirects the user to the log in flow.
      - Click Contact us button expands the iframe and allows user interaction 
        - This can be minimized/closed as well
- Onboarding flow
  - General case:
    - Given a user on a particular step of the flow 
      - When they submit their response (multiple input types) and click continue
      - Verify:
        - The flow displays the expected next step 
          - Verify using `data-step` attribute on the `sl-flow` div and the `data-semantic-id` in the child div
        - User response has been logged
          - Verify in localStorage `sl-answers` the json object contains the response 
    - Given a user when they complete the entire flow
      Verify: 
      - The sleep score results is displayed
          - `<div class=sl-report>`
      - Tailor my program button exists and is active 
      - localStorage has `sent-report-xxx` and `sl-report-viewed-x-xxx` key with value True
  - Flow Order
    - How would you like to improve your sleep? checkboxes 
      - `div[data-semantic-id=improve_sleep]`
      - `<input type='checkbox'>`
    - How long have you had a problem with your sleep? 
      - `div[data-semantic-id=problem_sleep]`
      - `<select>`
    - Which of the following stops you from sleeping most often? radio button
      - `div[data-semantic-id=stop_sleeping]`
      - `<input type='radio'>`
    - To what extent has sleep troubled you in general? select
      - `div[data-semantic-id=troubled_in_general]`
      - `<select>`
    - How many nights a week have you had a problem with your sleep?
      - `div[data-semantic-id=problem_nights]`
      - `<select>`
    - How often have you felt that you were unable to control ... ? 
      - `div[data-semantic-id=unable_to_control]`
      - `<select>`
    - How likely is it that you would fall asleep during the day ... ? 
      - `div[data-semantic-id=fall_asleep_stay_awake]`
      - `<select>`
    - How would you describe your gender?
      - `div[data-semantic-id=gender]`
      - `<input type radio>`
    - What is your d.o.b.?
      - `div[data-semantic-id=date_of_birth]`
      - 3 `<select>` for month day year (built in validation)
    - What is your employment status?
      - `div[data-semantic-id=employment_status]`"
      - `<select>`
    - How much did poor sleep affect your productivity?
      - `div[data-semantic-id=affect_productivity]`
      - `<select>`
    - How many hours did you miss ... ?
      - `div[data-semantic-id=hours_missed]`
      - `<input type=number>`
    - Which of the following expert guides ... ? 
      - `div[data-semantic-id=expert_guides]`
      - `<input type='radio'>`
    - Get your sleep score
      - `div[data-semantic-id=new-sleepio-signup-optional-eligibility-v2]`
      - 4 `<input type=text>` First, Last, email, password
      - 2 `<input type=checkbox>` for Privacy & ToS and Acknowledgement  
      - Special Validations
        - Cannot register with a previously used email
        - localStorage `sl-v2-user-input` has inputs saved
        - localStorage `sl-sent-account-created-event` is True
        - localStorage `sl-ser-data` is True
  - Additional validation
    - Verify app calls `/api/serivce_method_proxy/RecordingAPI/2/post_events` for each condition
      - When a step is shown `action: 'viewed'`
      - When a user response is captured `action: 'created'` with  data in body -> fields -> value
      - When a step is completed (the user has responded) `action: 'completed'`
    - Verify when the entire flow is completed `/api/service_method_proxy/Answer/1/create_update_answers_bulk`
      - The request body contains a json object with all the responses. This should equal localStorage
    - Verify for each flow step the expected responses are available and selectable
    - Verify any input validation for the flow steps
      - Namely first and last name, password, email
      - But also selecting multiple check boxes and radio buttons when allowed

## Improvements Scenarios
- A progress bar across the top that allows the user to jump back and forth between steps would be nice