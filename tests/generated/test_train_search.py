import pytest
import allure
from pages.login_page import LoginPage
from pages.search_train_page import SearchTrainsPage


@allure.feature("IRCTC Train Search")
@allure.story("Search Trains")
@allure.title("Verify train search from Chennai (MS) to Bangalore (SBC) on 28/05/26")
@allure.description(
    "This test verifies that a user can search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/26. "
    "The test includes login with provided credentials and validates the search results."
)
@pytest.mark.train_search
@pytest.mark.smoke
@pytest.mark.regression
class TestTrainSearch:
    def test_search_train_from_chennai_to_bangalore(self, page):
        # Login to IRCTC
        login_page = LoginPage(page)
        
        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with provided credentials"):
            login_page.login("Dhiru_naughty", "DhirDhir@12")

        with allure.step("Verify login status"):
            assert login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty"

        # Search for trains
        search_page = SearchTrainsPage(page)

        with allure.step("Search trains from Chennai (MS) to Bangalore (SBC) on 28/05/26"):
            search_page.search_trains(
                source="MS",
                destination="SBC",
                date="28/05/2026",
                classes=None,
                general=None
            )

        with allure.step("Verify train search results are displayed"):
            assert search_page.is_search_results_displayed(), "Train search results are not displayed"
