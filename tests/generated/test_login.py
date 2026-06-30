import pytest
import allure
from pages.login_page import LoginPage


@allure.feature("IRCTC Login")
@allure.story("User Login")
@allure.title("Verify successful IRCTC login with valid credentials")
@allure.description("This test verifies that a user can log in to the IRCTC website using valid credentials.")
@pytest.mark.login
@pytest.mark.smoke
class TestIRCTCLogin:
    """Test suite for IRCTC login functionality."""

    def test_user_can_login_with_valid_credentials(self, page):
        """
        Verify that a user can log in to IRCTC with valid username and password.

        Test Steps:
        1. Load the IRCTC home/login page.
        2. Enter valid username and password.
        3. Perform login action.
        4. Verify successful login status.
        """
        # Initialize LoginPage
        login_page = LoginPage(page)

        # Step 1: Load the IRCTC home/login page
        with allure.step("Load IRCTC home/login page"):
            login_page.load_login_page()

        # Step 2: Login with valid credentials
        with allure.step("Login with valid credentials"):
            login_page.login("Dhiru_naughty", "DhirDhir@12")

        # Step 3: Verify login status
        with allure.step("Verify login status"):
            assert login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty"


# To run this test, use the following command:
# pytest test_login.py -v -m login --headed