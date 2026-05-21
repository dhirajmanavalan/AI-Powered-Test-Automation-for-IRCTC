import pytest
import allure
from pages.login_page import LoginPage
from pages.chart_vacancy_page import ChartsVacancy
from pages.mobile_pages.mobile_login_page import MobileLoginPage
from pages.mobile_pages.mobile_chart_vacancy_page import MobileChartsVacancyPage


@allure.feature("IRCTC Charts / Vacancy")
class TestChartVacancyDesktopUI:
    """
    Test cases for Charts / Vacancy functionality in desktop UI.
    """

    @pytest.mark.smoke
    @pytest.mark.train_search
    @pytest.mark.desktop
    @allure.story("Search Chart Vacancy by Train Number and Boarding Station")
    @allure.title("Verify chart vacancy search for train 12345 from Howrah HWH in desktop UI")
    @allure.description(
        "This test verifies that a user can search for chart vacancy using train number 12345 and boarding station Howrah (HWH) in the desktop UI."
    )
    def test_chart_vacancy_desktop_search(self, page):
        """
        Test chart vacancy search in desktop UI.
        Train number: 12345
        Boarding station: Howrah (HWH)
        """
        login_page = LoginPage(page)
        charts_page = ChartsVacancy(page)

        with allure.step("Load IRCTC home page"):
            login_page.load_login_page()

        with allure.step("Open Charts / Vacancy page"):
            charts_page.open_charts()

        with allure.step("Select train number 12345"):
            charts_page.select_train("12345")

        with allure.step("Select boarding station HWH (Howrah)"):
            charts_page.select_boarding_station("HWH")

        with allure.step("Verify chart result is displayed"):
            assert charts_page.is_chart_result_displayed()


@allure.feature("IRCTC Charts / Vacancy")
class TestChartVacancyMobileUI:
    """
    Test cases for Charts / Vacancy functionality in mobile UI.
    """

    @pytest.mark.smoke
    @pytest.mark.train_search
    @pytest.mark.mobile
    @allure.story("Search Chart Vacancy by Train Number and Boarding Station in Mobile UI")
    @allure.title("Verify chart vacancy search for train 12345 from Howrah HWH in mobile UI")
    @allure.description(
        "This test verifies that a user can search for chart vacancy using train number 12345 and boarding station Howrah (HWH) in the mobile UI."
    )
    def test_chart_vacancy_mobile_search(self, mobile_page):
        """
        Test chart vacancy search in mobile UI.
        Train number: 12345
        Boarding station: Howrah (HWH)
        """
        mobile_login_page = MobileLoginPage(mobile_page)
        mobile_charts_page = MobileChartsVacancyPage(mobile_page)

        with allure.step("Load IRCTC home page in mobile view"):
            mobile_login_page.load_login_page()

        with allure.step("Open Charts / Vacancy page in mobile view"):
            mobile_charts_page.open_charts()

        with allure.step("Select train number 12345 in mobile view"):
            mobile_charts_page.select_train("12345")

        with allure.step("Select boarding station HWH (Howrah) in mobile view"):
            mobile_charts_page.select_boarding_station("HWH")

        with allure.step("Verify chart result is displayed in mobile view"):
            assert mobile_charts_page.is_chart_result_displayed()