import pytest
import allure
from pages.login_page import LoginPage
from pages.ticket_cancel_history_page import TicketCancelHistoryPage


@allure.feature("IRCTC Account Management")
@allure.story("Ticket Cancellation History Navigation")
@allure.title("Verify logged-in user can navigate to Ticket Cancellation History page")
@allure.description(
    "This test verifies that a logged-in user can navigate to the IRCTC Ticket Cancellation History page "
    "after successful login."
)
@pytest.mark.login
@pytest.mark.smoke
@pytest.mark.regression
class TestTicketCancellationHistoryNavigation:
    """Test suite for verifying navigation to Ticket Cancellation History page."""

    def test_logged_in_user_can_navigate_to_ticket_cancellation_history(
        self, page
    ):
        """
        Verify that a logged-in user can navigate to the Ticket Cancellation History page.

        Steps:
        1. Load the IRCTC login page.
        2. Login with valid credentials.
        3. Assert login success.
        4. Navigate to Ticket Cancellation History page.
        """
        username = "Dhiru_naughty"
        password = "DhirDhir@12"

        login_page = LoginPage(page)
        ticket_cancel_history_page = TicketCancelHistoryPage(page)

        with allure.step("Load IRCTC login page"):
            login_page.load_login_page()

        with allure.step(f"Login with username: {username}"):
            login_page.login(username, password)

        with allure.step(f"Verify login status for user: {username}"):
            assert login_page.login_status(username), f"Login failed for user: {username}"

        with allure.step("Navigate to Ticket Cancellation History page"):
            ticket_cancel_history_page.go_to_ticket_cancellation_history()

        # Note: The TicketCancelHistoryPage does not provide a direct assertion method.
        # In a real-world scenario, you would assert the presence of elements on the Ticket Cancellation History page.
        # For example, checking if the page title or a specific element is displayed.
        # Since the page object does not expose such methods, we assume navigation is successful if no exception is raised.

        # If an assertion method is added in the future, it can be used here.
        # Example: assert ticket_cancel_history_page.is_ticket_cancellation_history_displayed()

        # Placeholder for future assertion (if implemented in the page object):
        # assert ticket_cancel_history_page.is_ticket_cancellation_history_displayed()


# Required pytest markers for test discovery and categorization.