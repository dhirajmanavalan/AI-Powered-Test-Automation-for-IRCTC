import pytest
import allure
from pages.mobile_pages.mobile_login_page import MobileLoginPage
from pages.mobile_pages.mobile_search_page import MobileSearchTrainsPage


@allure.feature("IRCTC Mobile Train Search")
@allure.story("Search Trains in Mobile View")
@allure.title("Verify train search from Chennai to Bangalore in mobile view")
@allure.description(
    "This test verifies that a user can search for trains from Chennai (MS) to Bangalore (SBC) "
    "on a mobile device using the provided credentials."
)
@pytest.mark.mobile
@pytest.mark.train_search
@pytest.mark.smoke
class TestMobileTrainSearch:
    """Test suite for mobile train search functionality."""

    def test_search_train_mobile_view(self, mobile_page):
        """
        Test Case: Search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026 in mobile view.

        Steps:
        1. Load the IRCTC mobile home page.
        2. Login with the provided credentials.
        3. Verify login success.
        4. Search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026.
        5. Verify search results are displayed.
        """
        login_page = MobileLoginPage(mobile_page)
        search_page = MobileSearchTrainsPage(mobile_page)

        with allure.step("Load IRCTC mobile home page"):
            login_page.load_login_page()

        with allure.step("Login with provided credentials"):
            login_page.login("Dhiru_naughty", "DhirDhir@12")

        with allure.step("Verify login status"):
            assert login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty"

        with allure.step("Search trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026"):
            search_page.search_trains(
                source="MS",
                destination="SBC",
                date="28/05/2026",
                classes=None,
                general=None
            )

        with allure.step("Verify train search results are displayed"):
            assert search_page.is_search_results_displayed(), "Train search results are not displayed"