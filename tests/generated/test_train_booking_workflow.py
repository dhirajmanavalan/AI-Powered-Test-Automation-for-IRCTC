import pytest
import allure
from pages.login_page import LoginPage
from pages.search_train_page import SearchTrainsPage
from pages.booking_page import BookingPage
from pages.passenger_details_page import PassengerDetailsPage
from pages.mobile_pages.mobile_login_page import MobileLoginPage
from pages.mobile_pages.mobile_search_page import MobileSearchTrainsPage
from pages.mobile_pages.mobile_booking_page import MobileBookingPage


@allure.feature("IRCTC Train Booking")
class TestDesktopTrainBookingWorkflow:
    """
    Test suite for desktop UI train booking workflow.
    Includes login, train search, selection, and booking initiation.
    """

    @pytest.fixture
    def setup_desktop(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.search_page = SearchTrainsPage(page)
        self.booking_page = BookingPage(page)

    @allure.story("Desktop UI: Login and Book Train")
    @allure.title("Verify successful train booking workflow in desktop UI")
    @allure.description(
        "This test verifies the complete train booking workflow in desktop UI: "
        "login, search trains from Chennai to Bangalore, select a train, and initiate booking."
    )
    @pytest.mark.login
    @pytest.mark.train_search
    @pytest.mark.smoke
    def test_desktop_train_booking_workflow(self, setup_desktop):
        with allure.step("Load IRCTC home page"):
            self.login_page.load_login_page()

        with allure.step("Login with provided credentials"):
            self.login_page.login("Dhiru_naughty", "DhirDhir@12")
            assert self.login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty"

        with allure.step("Search trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026"):
            self.search_page.search_trains(
                source="MS",
                destination="SBC",
                date="28/05/2026",
                classes="SL",
                general="GENERAL"
            )
            assert self.search_page.is_search_results_displayed(), "Train search results not displayed"

        with allure.step("Select a train with availability and initiate booking"):
            self.booking_page.select_train_based_on_availability(
                input_date="28/05/2026",
                preferred_class="SL"
            )


@allure.feature("IRCTC Mobile Train Booking")
class TestMobileTrainBookingWorkflow:
    """
    Test suite for mobile UI train booking workflow.
    Includes login, train search, selection, and booking initiation.
    """

    @pytest.fixture
    def setup_mobile(self, mobile_page):
        self.page = mobile_page
        self.login_page = MobileLoginPage(mobile_page)
        self.search_page = MobileSearchTrainsPage(mobile_page)
        self.booking_page = MobileBookingPage(mobile_page)

    @allure.story("Mobile UI: Login and Book Train")
    @allure.title("Verify successful train booking workflow in mobile UI")
    @allure.description(
        "This test verifies the complete train booking workflow in mobile UI: "
        "login, search trains from Chennai to Bangalore, select a train, and initiate booking."
    )
    @pytest.mark.login
    @pytest.mark.train_search
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_mobile_train_booking_workflow(self, setup_mobile):
        with allure.step("Load IRCTC home page in mobile view"):
            self.login_page.load_login_page()

        with allure.step("Login with provided credentials in mobile view"):
            self.login_page.login("Dhiru_naughty", "DhirDhir@12")
            assert self.login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty in mobile view"

        with allure.step("Search trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026 in mobile view"):
            self.search_page.search_trains(
                source="MS",
                destination="SBC",
                date="28/05/2026",
                classes="SL",
                general="GENERAL"
            )
            assert self.search_page.is_search_results_displayed(), "Train search results not displayed in mobile view"

        with allure.step("Select a train with availability and initiate booking in mobile view"):
            self.booking_page.select_train_based_on_availability(
                input_date="28/05/2026",
                preferred_class="SL"
            )