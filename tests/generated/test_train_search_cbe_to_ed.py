import pytest
import allure
from pages.login_page import LoginPage
from pages.search_train_page import SearchTrainsPage


@allure.feature("IRCTC Train Search")
@allure.story("Search Trains")
@allure.title("Verify train search from Coimbatore (CBE) to Erode (ED)")
@allure.description(
    "This test verifies that trains can be searched from Coimbatore (CBE) to Erode (ED). "
    "The test ensures that the search results are displayed correctly."
)
@pytest.mark.train_search
@pytest.mark.smoke
@pytest.mark.regression
class TestTrainSearchCBEDToED:
    """Test suite for verifying train search from Coimbatore (CBE) to Erode (ED)."""

    def test_verify_train_search_cbe_to_ed(self, page):
        """
        Verify train search from Coimbatore (CBE) to Erode (ED).
        
        Steps:
        1. Load the IRCTC home page.
        2. Search for trains from CBE to ED.
        3. Assert that search results are displayed.
        """
        login_page = LoginPage(page)
        search_page = SearchTrainsPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Search trains from Coimbatore (CBE) to Erode (ED)"):
            search_page.search_trains(
                source="CBE",
                destination="ED",
                date=None,
                classes=None,
                general=None
            )

        with allure.step("Verify that train search results are displayed"):
            assert search_page.is_search_results_displayed(), "Train search results are not displayed."