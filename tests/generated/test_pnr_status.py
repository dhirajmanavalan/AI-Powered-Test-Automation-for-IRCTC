import pytest
import allure
from pages.pnr_status_page import PNRStatusPage
from pages.mobile_pages.mobile_pnr_status_page import MobilePNRStatusPage

from pages.login_page import LoginPage
from pages.mobile_pages.mobile_login_page import MobileLoginPage


@allure.feature("IRCTC PNR Status")
class TestPNRStatusDesktopUI:
    """
    Test PNR Status for Desktop UI.
    """

    @allure.story("Check PNR Status in Desktop UI")
    @allure.title("Verify PNR status enquiry for valid PNR in Desktop UI")
    @allure.description("This test verifies that a user can check PNR status using a valid PNR number in Desktop UI.")
    @pytest.mark.pnr_status
    @pytest.mark.desktop
    @pytest.mark.smoke
    def test_pnr_status_desktop_ui(self, page):
        """
        Test PNR status enquiry for valid PNR number in Desktop UI.
        """
        pnr_number = "4136773029"

        pnr_page = PNRStatusPage(page)
        login_page = LoginPage(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step(f"Check PNR status for PNR: {pnr_number}"):
            pnr_page.pnr_status(pnr_number)

        with allure.step("Verify PNR status is displayed"):
            assert not pnr_page.is_pnr_status_displayed(pnr_number), "PNR status should be displayed"


@allure.feature("IRCTC PNR Status")
class TestPNRStatusMobileUI:
    """
    Test PNR Status for Mobile UI.
    """

    @allure.story("Check PNR Status in Mobile UI")
    @allure.title("Verify PNR status enquiry for valid PNR in Mobile UI")
    @allure.description("This test verifies that a user can check PNR status using a valid PNR number in Mobile UI.")
    @pytest.mark.pnr_status
    @pytest.mark.mobile
    @pytest.mark.smoke
    def test_pnr_status_mobile_ui(self, mobile_page):
        """
        Test PNR status enquiry for valid PNR number in Mobile UI.
        """
        pnr_number = "4136773029"

        mobile_pnr_page = MobilePNRStatusPage(mobile_page)
        mobile_login_page = MobileLoginPage(mobile_page)

        with allure.step("Load IRCTC home page in Mobile view"):
            mobile_login_page.load_login_page()

        with allure.step(f"Check PNR status for PNR: {pnr_number}"):
            mobile_pnr_page.pnr_status(pnr_number)

        with allure.step("Verify PNR status is displayed"):
            assert not mobile_pnr_page.is_pnr_status_displayed(pnr_number), "PNR status should be displayed"
