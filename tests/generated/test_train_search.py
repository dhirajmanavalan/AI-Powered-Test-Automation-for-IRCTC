import pytest
import allure
from pages.login_page import LoginPage
from pages.search_train_page import SearchTrainsPage


@allure.feature("IRCTC Train Search")
@allure.story("Search Trains")
@allure.title("Verify train search from MAS to YPR on 26/06/2026 in SL class under GENERAL quota")
@allure.description(
    "This test verifies that trains can be searched from MAS to YPR on 26/06/2026 "
    "in SL class under GENERAL quota."
)
@pytest.mark.train_search
@pytest.mark.smoke
@pytest.mark.regression
class TestTrainSearchFromMASToYPR:
    """Test suite for verifying train search from MAS to YPR."""

    def test_search_trains_mas_to_ypr(self, page):
        """Test to verify train search from MAS to YPR on 26/06/2026 in SL class under GENERAL quota."""
        login_page = LoginPage(page)
        search_page = SearchTrainsPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step(
            "Search trains from MAS to YPR on 26/06/2026 in SL class under GENERAL quota"
        ):
            search_page.search_trains(
                source="MAS",
                destination="YPR",
                date="26/06/2026",
                classes="SL",
                general="GENERAL"
            )

        with allure.step("Verify train search results are displayed"):
            assert search_page.is_search_results_displayed(), "Train search results are not displayed"
