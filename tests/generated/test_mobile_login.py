import pytest
import allure
from pages.mobile_pages.mobile_login_page import MobileLoginPage


@allure.feature("IRCTC Mobile Login")
@allure.story("Mobile User Login")
@allure.title("Verify successful mobile login with valid credentials")
@allure.description(
    "This test verifies that a user can log in to the IRCTC mobile view using valid credentials."
)
@pytest.mark.mobile
@pytest.mark.login
@pytest.mark.smoke
class TestMobileLogin:
    """Test suite for IRCTC mobile login functionality."""

    def test_mobile_login_success(self, mobile_page):
        """
        Test Case: Mobile Login
        Steps:
        1. Load the IRCTC mobile home page.
        2. Login with valid credentials.
        3. Verify login status.
        """
        username = "Dhiru_naughty"
        password = "DhirDhir@12"

        login_page = MobileLoginPage(mobile_page)

        with allure.step("Load IRCTC mobile home page"):
            login_page.load_login_page()

        with allure.step("Login with valid credentials"):
            login_page.login(username, password)

        with allure.step("Verify login status"):
            assert login_page.login_status(username), "Login failed for user: " + username