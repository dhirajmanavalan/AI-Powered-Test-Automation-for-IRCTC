import pytest
import allure
from pages.login_page import LoginPage

@allure.feature("IRCTC Login")
class TestIRCTCLogin:
    """Test suite for IRCTC login functionality."""

    @pytest.mark.login
    @pytest.mark.smoke
    @allure.story("Valid Login")
    @allure.title("Verify successful login with valid credentials")
    @allure.description("This test verifies that a user can log in to the IRCTC website using valid credentials.")
    def test_valid_login(self, page):
        """Test case to verify successful login with valid credentials."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with valid credentials"):
            login_page.login("valid_username", "valid_password")

        with allure.step("Verify login status"):
            assert login_page.login_status("valid_username"), "Login failed with valid credentials"

    @pytest.mark.login
    @pytest.mark.regression
    @allure.story("Invalid Password")
    @allure.title("Verify login fails with invalid password")
    @allure.description("This test verifies that login fails when an invalid password is provided.")
    def test_login_with_invalid_password(self, page):
        """Test case to verify login fails with invalid password."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with invalid password"):
            login_page.login("valid_username", "invalid_password")

        with allure.step("Verify login status"):
            assert not login_page.login_status("valid_username"), "Login succeeded with invalid password"

    @pytest.mark.login
    @pytest.mark.regression
    @allure.story("Invalid Username")
    @allure.title("Verify login fails with invalid username")
    @allure.description("This test verifies that login fails when an invalid username is provided.")
    def test_login_with_invalid_username(self, page):
        """Test case to verify login fails with invalid username."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with invalid username"):
            login_page.login("invalid_username", "valid_password")

        with allure.step("Verify login status"):
            assert not login_page.login_status("invalid_username"), "Login succeeded with invalid username"

    @pytest.mark.login
    @pytest.mark.regression
    @allure.story("Empty Username")
    @allure.title("Verify login fails with empty username")
    @allure.description("This test verifies that login fails when the username field is left empty.")
    def test_login_with_empty_username(self, page):
        """Test case to verify login fails with empty username."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with empty username"):
            login_page.login("", "valid_password")

        with allure.step("Verify login status"):
            assert not login_page.login_status(""), "Login succeeded with empty username"

    @pytest.mark.login
    @pytest.mark.regression
    @allure.story("Empty Password")
    @allure.title("Verify login fails with empty password")
    @allure.description("This test verifies that login fails when the password field is left empty.")
    def test_login_with_empty_password(self, page):
        """Test case to verify login fails with empty password."""
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Login with empty password"):
            login_page.login("valid_username", "")

        with allure.step("Verify login status"):
            assert not login_page.login_status("valid_username"), "Login succeeded with empty password"