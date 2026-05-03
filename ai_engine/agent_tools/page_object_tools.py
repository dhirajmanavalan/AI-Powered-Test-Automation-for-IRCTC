from utils.logger import get_logger
logger = get_logger()

PNR_STATUS_PAGE_RULE_SET = """
==================================================
3. PNRStatusPage
==================================================
Import:
from pages.pnr_status_page import PNRStatusPage

Purpose:
PNRStatusPage is used to check the status of a valid pnr_number.

Methods:
- pnr_status(self,pnr_number:str)-> None:
- is_pnr_status_displayed(self,pnr_number)-> bool:
    Returns True if valid PNR status is displayed, otherwise returns False.

PNRStatusPage Rules:
- Login is not required to check PNR Status search.
"""
SEARCH_TRAIN_PAGE_RULE_SET = """
==================================================
2. SearchTrainsPage
==================================================

Import:
from pages.search_train_page import SearchTrainsPage

Purpose:
SearchTrainsPage is used to search trains from a source station to a destination station.

Methods:
- search_trains(
      source: str,
      destination: str,
      date: str = None,
      classes: str = None,
      general: str = None
  ) -> None
    Searches trains using source, destination, journey date, travel class, and quota/category.

- is_search_results_displayed() -> bool
    Returns True if train search results are displayed, otherwise returns False.

Parameter Details:
- source:
    Source station name or station code.
    Example: "KGP"

- destination:
    Destination station name or station code.
    Example: "YPR"

- date:
    Journey date.
    This parameter is optional.
    If the user provides a date, pass that value.
    If the user does not provide a date, pass None.

- classes:
    Travel class.
    This parameter is optional.
    If the user provides a class, pass that value.
    If the user does not provide a class, pass None.

- general:
    Quota/category.
    This parameter is optional.
    If the user provides a quota/category, pass that value.
    If the user does not provide a quota/category, pass None.
    
SearchTrainsPage Rules:
- Login is optional for train search.
- Default behavior: generate train search tests without login.
- If the user provides username and password, include login before searching trains.
- If the user does not provide username and password, do not call login().
- Always use search_trains() for train search scenarios.
- Use is_search_results_displayed() to assert that train search results are displayed.
- Do not invent extra SearchTrainsPage methods.
- Do not write raw Playwright locators in generated tests.

Example Usage Without Login:
login_page = LoginPage(page)
login_page.load_login_page()

search_page = SearchTrainsPage(page)
search_page.search_trains(
    source="KGP",
    destination="YPR",
    date=None,
    classes=None,
    general=None
)

assert search_page.is_search_results_displayed()

Example Usage With Login:
login_page = LoginPage(page)
login_page.load_login_page()
login_page.login("username", "password")
assert login_page.login_status("username")

search_page = SearchTrainsPage(page)
search_page.search_trains(
    source="KGP",
    destination="YPR",
    date=None,
    classes=None,
    general=None
)

assert search_page.is_search_results_displayed()
"""
LOGIN_PAGE_RULE_SET = """
==================================================
1. LoginPage
==================================================

Import:
from pages.login_page import LoginPage

Purpose:
LoginPage is used to load the IRCTC home/login page and perform login-related actions.

Methods:
- load_login_page() -> None
    Loads the IRCTC home page. This should be used as the first step in every generated test case.

- login(name: str, password: str) -> None
    Enters username and password and performs the login action.

- login_status(name: str) -> bool
    Returns True if login is successful for the given user name, otherwise returns False.

LoginPage Rules:
- Do not include assertion to verify whether the URL is redirected to Dashboard.
- Use login_status(name) method to assert login success.
- Do not write raw Playwright locators in generated tests.
- Do not hardcode real credentials unless the user explicitly provides them.
- If credentials are not provided, use placeholder values such as "username" and "password".
"""
TICKET_CANCELLATION_HISTORY_RULE_SET = """
==================================================
1. TicketCancelHistoryPage
==================================================

Import:
from pages.ticket_cancel_history_page import TicketCancelHistoryPage

Purpose:
TicketCancelHistoryPage is used to navigate to the IRCTC Ticket Cancellation History page.

Functional Description:
This page object handles the navigation flow from the logged-in IRCTC home/account area to the Ticket Cancellation History page.

Navigation Flow:
1. Click MY ACCOUNT.
2. Hover over My Transactions.
3. Click Ticket Cancellation History.

Methods:
- go_to_ticket_cancellation_history() -> None
    Navigates to the Ticket Cancellation History page by clicking MY ACCOUNT,
    hovering over My Transactions, and clicking Ticket Cancellation History.

TicketCancelHistoryPage Rules:
- Use this page object only for ticket cancellation history navigation scenarios.
- User should normally be logged in before using this page object, because MY ACCOUNT and transaction history are account-specific.
"""
CHART_VACANCY_PAGE_RULE_SET = """
==================================================
ChartsVacancy Page Object
==================================================

Import:
from pages.chart_vacancy_page import ChartsVacancy

Purpose:
ChartsVacancy is used to open the IRCTC Charts / Vacancy page in a new browser tab and search train chart/vacancy details using train number and boarding station.

Methods:
- open_charts() -> None
    Clicks the "CHARTS / VACANCY" option from the IRCTC home page.
    This opens the Charts / Vacancy page in a new tab.
    The new tab is stored internally as self.new_tab.

- select_train(train_number: str) -> None
    Enters the train number into the train search input on the Charts / Vacancy page.
    Example:
    select_train("12863")

- select_boarding_station(boarding_station_code: str) -> None
    Selects the boarding station using station code and clicks "Get Train Chart".
    Example:
    select_boarding_station("HWH")

- is_chart_result_displayed() -> bool
    Verifies whether the chart/vacancy result flow completed.
    Returns True if either:
    1. The "Chart not prepared" popup/message is visible, or
    2. The page URL changes to the train composition result page containing "charts/traincomposition".
    Returns False if the expected result page is not displayed within timeout.

ChartsVacancy Rules:
- Use ChartsVacancy for Charts / Vacancy test scenarios.
- As the first step, use LoginPage.load_login_page() to load the IRCTC home page.
- Login is not required for Charts / Vacancy search unless the user explicitly asks for login.
- Call open_charts() before calling select_train() or select_boarding_station().
- Call select_train(train_number) before select_boarding_station(boarding_station_code).
- After open_charts(), the page object handles the new tab internally using self.new_tab.
- Do not pass page or new_tab from the test case to ChartsVacancy methods.
- Do not write raw Playwright locators in generated tests.
- Do not invent extra methods that are not listed here.
- Always assert Charts / Vacancy scenarios using is_chart_result_displayed().
- A "Chart not prepared" message should be treated as a valid displayed result because the application responded to the search.

Required Parameters:
- train_number:
    Train number as string.
    Example: "12863"

- boarding_station_code:
    Boarding station code as string.
    Example: "HWH"

Example Usage:
login_page = LoginPage(page)
login_page.load_login_page()

charts_page = ChartsVacancy(page)
charts_page.open_charts()
charts_page.select_train("12863")
charts_page.select_boarding_station("HWH")

assert charts_page.is_chart_result_displayed()
"""
TRAIN_BOOKING_PAGE_RULE_SET = """
==================================================
BookingPage Page Object
==================================================

Import:
from pages.booking_page import BookingPage

Purpose:
BookingPage is used to select a train from the train availability results and proceed with booking by clicking the available "Book Now" option.

Important Workflow Dependency:
BookingPage should be used only after:
1. LoginPage is used to load the IRCTC home page.
2. User login is completed.
3. SearchTrainsPage is used to search train availability.
4. Train search results are displayed on the train-list page.

Methods:
- select_train_based_on_availability(input_date: str, preferred_class: str = "SL") -> None
    Selects a train based on seat availability for the given journey date and preferred class.
    It checks available train cards, selects the preferred class, checks the date availability block,
    skips unavailable trains, and clicks the enabled "Book Now" button for a valid train.
    It also handles the confirmation popup if it appears.

Parameter Details:
- input_date:
    Journey date in dd/mm/yyyy format.
    Example: "26/06/2026"

- preferred_class:
    Preferred travel class.
    Default value: "SL"

    Supported values:
    - "SL"  for Sleeper
    - "3A"  for AC 3 Tier
    - "2A"  for AC 2 Tier
    - "1A"  for AC First Class
    - "3E"  for AC 3 Economy
    - "CC"  for Chair Car
    - "EC"  for Executive Chair Car
    - "2S"  for Second Sitting
    
BookingPage Rules:
- Use BookingPage only for train booking scenarios.
- To book a train, the user should be logged in first using LoginPage.
- Before using BookingPage, search train availability using SearchTrainsPage.
- After login and train search, call select_train_based_on_availability().
- Do not use BookingPage before SearchTrainsPage.
- Do not write raw Playwright locators in generated tests.
- Do not call BookingPage helper/private methods directly.
- Do not call methods whose names start with underscore.
- Do not call wait_for_results() directly.
- Do not call handle_confirmation_popup_if_present() directly.
- Do not invent validation/assertion methods for BookingPage.
- Do not perform payment confirmation.
- Stop the booking flow after BookingPage clicks Book Now and handles confirmation if present.
- If the user does not provide preferred class, use "SL" as default.
- If the user provides a class, use that class as preferred_class.
- If the user provides journey date in short format such as "26/06/26", convert it to "26/06/2026" before passing it to BookingPage.
- The input_date value passed to select_train_based_on_availability() must be the same as the date value passed to SearchTrainsPage.search_trains().
- The preferred_class value passed to select_train_based_on_availability() must be the same as the classes value passed to SearchTrainsPage.search_trains().
- Do not use different date or class values between SearchTrainsPage and BookingPage.
- The value passed to BookingPage.select_train_based_on_availability(
      input_date,
      preferred_class
  )
  must be the same as the values passed to SearchTrainsPage.search_trains(
      date,
      classes
  ).

- Mapping rule:
  - input_date must use the same value as search_trains(date=...)
  - preferred_class must use the same value as search_trains(classes=...)

- Do not generate different date or class values between SearchTrainsPage and BookingPage.

Correct Example:
search_page.search_trains(
    source="HWH",
    destination="YPR",
    date="26/06/2026",
    classes="SL",
    general="GENERAL"
)

booking_page.select_train_based_on_availability(
    input_date="26/06/2026",
    preferred_class="SL"
)

Incorrect Example:
search_page.search_trains(
    source="HWH",
    destination="YPR",
    date="26/06/2026",
    classes="SL",
    general="GENERAL"
)

booking_page.select_train_based_on_availability(
    input_date="27/06/2026",
    preferred_class="3A"
)

"""



MOBILE_DEVICE_LOGIN_PAGE_RULE_SET = """
==================================================
1. MobileLoginPage
==================================================

Import:
from pages.mobile_pages.mobile_login_page import MobileLoginPage

Purpose:
LoginPage is used to load the IRCTC home/login page and perform login-related actions.

Methods:
- load_login_page() -> None
    Loads the IRCTC home page. This should be used as the first step in every generated test case.

- login(name: str, password: str) -> None
    Enters username and password and performs the login action.

- login_status(name: str) -> bool
    Returns True if login is successful for the given user name, otherwise returns False.

MobileLoginPage Rules:
- Do not include assertion to verify whether the URL is redirected to Dashboard.
- Use login_status(name) method to assert login success.
- Do not write raw Playwright locators in generated tests.
- Do not hardcode real credentials unless the user explicitly provides them.
- If credentials are not provided, use placeholder values such as "username" and "password".
"""
MOBILE_DEVICE_PNR_STATUS_PAGE_RULE_SET = """
==================================================
3. MobilePNRStatusPage
==================================================
Import:
from  pages.mobile_pages.mobile_pnr_status_page import MobilePNRStatusPage

Purpose:
PNRStatusPage is used to check the status of a valid pnr_number.
It check PNR Status in mobile UI

Methods:
- pnr_status(self,pnr_number:str)-> None:
- is_pnr_status_displayed(self,pnr_number)-> bool:
    Returns True if valid PNR status is displayed, otherwise returns False.

PNRStatusPage Rules:
- Login is not required to check PNR Status search.
"""



def get_available_page_objects() -> str:
    """
    Returns available Page Object Model classes and methods.

    This helps the test generation agent generate tests using the
    existing Page Object Model instead of raw locators.
    """

    logger.info("Tool called: get_available_page_objects")

    return f"""
Available Page Object Classes:
{LOGIN_PAGE_RULE_SET}
{SEARCH_TRAIN_PAGE_RULE_SET}
{PNR_STATUS_PAGE_RULE_SET}
{TICKET_CANCELLATION_HISTORY_RULE_SET}
{CHART_VACANCY_PAGE_RULE_SET}
{TRAIN_BOOKING_PAGE_RULE_SET}

Available Mobile Page Object Classes:
{MOBILE_DEVICE_LOGIN_PAGE_RULE_SET}
{MOBILE_DEVICE_PNR_STATUS_PAGE_RULE_SET}

==================================================
Global Rules
==================================================
- For mobile pages use mobile_page as parameter in the generated test cases.
- Use only the available Page Object Model classes and methods listed above.
- Avoid raw Playwright locators in generated tests.
- Do not perform real payment confirmation.
- As the first step for every generated test case, use load_login_page() from LoginPage because it loads the home page.
- As the first step for every generated test case for mobile pages, use load_login_page() from MobileLoginPage because it loads the home page in mobile view.
- If a specific Page Object rule conflicts with a global rule, prioritize the specific Page Object rule.
- Do not invent methods that are not listed in this tool response.
- Keep generated tests readable and pytest-compatible.

==================================================
Pytest Marker Rules
==================================================
- Every generated test case must include suitable pytest markers.
- Use marker names based on the test purpose.
- Examples:
  - @pytest.mark.login for login tests
  - @pytest.mark.train_search for train search tests
  - @pytest.mark.pnr_status for PNR status tests
  - @pytest.mark.smoke for critical happy-path tests
  - @pytest.mark.regression for broader regression tests
  - @pytest.mark.mobile for mobile tests
- Use lowercase marker names only.
- Use underscores for multi-word marker names.
- Do not use spaces or hyphens in marker names.

==================================================
Allure Annotation Rules
==================================================
- Every generated test file must import allure if Allure annotations are used.
- Add suitable Allure annotations to every generated test class or test function.
- Use @allure.feature(...) to describe the major application feature.
- Use @allure.story(...) to describe the specific user workflow.
- Use @allure.title(...) to provide a readable test title.
- Use @allure.description(...) to explain what the test validates.
- Use allure.step(...) context blocks for important test actions.
- Keep Allure names readable and business-friendly.
- Do not use raw locators inside Allure steps.
- Allure annotations should match the pytest markers and test purpose.

Allure Annotation Examples:
- For login tests:
  @allure.feature("IRCTC Login")
  @allure.story("User Login")
  @allure.title("Verify successful IRCTC login")
  @allure.description("This test verifies that a user can log in to the IRCTC website using valid credentials.")

- For train search tests:
  @allure.feature("IRCTC Train Search")
  @allure.story("Search Trains")
  @allure.title("Verify train search from source to destination")
  @allure.description("This test verifies that trains can be searched using source, destination, date, class, and quota.")

- For PNR status tests:
  @allure.feature("IRCTC PNR Status")
  @allure.story("Check PNR Status")
  @allure.title("Verify PNR status enquiry")
  @allure.description("This test verifies that a user can check PNR status using a valid PNR number.")

- For mobile tests:
  @allure.feature("IRCTC Mobile")
  @allure.story("Mobile Login or Mobile Workflow")
  @allure.title("Verify IRCTC workflow in mobile view")
  @allure.description("This test verifies the selected IRCTC workflow using the mobile page fixture.")

Generated Test Structure Rule:
- For every major action, wrap the Page Object method call inside allure.step().
- Example:
  with allure.step("Load IRCTC home page"):
      login_page.load_login_page()

  with allure.step("Login with valid credentials"):
      login_page.login("username", "password")

  with allure.step("Verify login status"):
      assert login_page.login_status("username")
"""

if __name__=="__main__":
    # FOR DEBUGING
    print(get_available_page_objects())

