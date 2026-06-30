import pytest
import allure
from pages.login_page import LoginPage
from pages.chart_vacancy_page import ChartsVacancy


@allure.feature("IRCTC Charts/Vacancy")
@allure.story("Verify Charts and Vacancy Details")
@allure.title("Verify charts and vacancy details for train number 22668 with boarding station CBE")
@allure.description("This test verifies that the charts and vacancy details for train number 22668 with boarding station CBE can be retrieved successfully.")
@pytest.mark.charts_vacancy
@pytest.mark.smoke
@pytest.mark.regression
class TestChartsVacancy:
    @allure.step("Load IRCTC home page")
    def test_verify_charts_vacancy_details(self, page):
        login_page = LoginPage(page)
        login_page.load_login_page()

        charts_page = ChartsVacancy(page)
        charts_page.open_charts()

        with allure.step("Select train number 22668"):
            charts_page.select_train("22668")

        with allure.step("Select boarding station CBE"):
            charts_page.select_boarding_station("CBE")

        with allure.step("Verify chart result is displayed"):
            assert charts_page.is_chart_result_displayed()