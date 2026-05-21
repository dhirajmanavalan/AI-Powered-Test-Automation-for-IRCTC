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

    def test_successful_login(self, page):
        """Test successful login with valid credentials."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home/login page"):
            login_page.load_login_page()

        with allure.step("Login with valid credentials"):
            login_page.login("Dhiru_naughty", "DhirDhir@12")

        with allure.step("Verify login status"):
            assert login_page.login_status("Dhiru_naughty"), "Login failed for user Dhiru_naughty"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])