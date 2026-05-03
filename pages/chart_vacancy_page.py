from playwright.sync_api import Page,expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re
from utils.logger import get_logger

logger = get_logger()
class ChartsVacancy:

    def __init__(self, page: Page):
        self.page = page
        self.context = page.context
        self.new_tab: Page | None = None

    # LOCATORS
    CHART_BUTTON = "(//label[normalize-space()='CHARTS / VACANCY'])[1]"
    TRAIN_NUMBER = "(//input[contains(@id,'react-select')])[1]"
    BOARDING_STATION = "//div[text()='Boarding Station*']"
    BOARDING_STATION_INPUT = "//div[@id='boardingStation']//input[contains(@id,'react-select')]"
    TRAIN_CHART = "//span[normalize-space()='Get Train Chart']"
    CHART_NOT_PREPARED_POP_UP = "//span[contains(text(), 'Chart not prepared')]"

    def open_charts(self):
        # Click and capture new tab
        with self.context.expect_page() as new_page_info:
            self.page.locator(self.CHART_BUTTON).click()

        self.new_tab = new_page_info.value
        self.new_tab.wait_for_load_state()

        print("Charts Page Title:", self.new_tab.title())

    def select_train(self,train_number):
        train_input = self.new_tab.locator(self.TRAIN_NUMBER)
        train_input.wait_for(state="visible")

        # I/P : Type train number
        train_input.type(train_number, delay=100)
        train_input.press("Enter")

    def select_boarding_station(self,boarding_station_code):
        # Step 1: Click boarding station input
        self.new_tab.locator(self.BOARDING_STATION).click()
        boarding_input = self.new_tab.locator(self.BOARDING_STATION_INPUT)
        boarding_input.clear()
        # I/P : Type train number
        boarding_input.fill(boarding_station_code)
        boarding_input.press("Enter")

        self.new_tab.locator(self.TRAIN_CHART).click()

    def is_chart_result_displayed(self) -> bool:
        """
        Checks whether the chart/vacancy result is displayed.
        """

        if self.new_tab is None:
            logger.error("Charts page is not opened. Call open_charts() first.")
            return False

        try:
            chart_not_prep = self.new_tab.locator(self.CHART_NOT_PREPARED_POP_UP)
            chart_not_prep.wait_for(state="visible", timeout=3000)

            if chart_not_prep.is_visible():
                logger.info("Chart not prepared message is visible")
                return True

        except PlaywrightTimeoutError:
            logger.info("Chart not prepared message not visible. Checking result URL.")

        try:
            self.new_tab.wait_for_url(
                "**charts/traincomposition**",
                timeout=5000
            )

            expect(self.new_tab).to_have_url(
                re.compile(r".*charts/traincomposition.*")
            )

            logger.info("Train composition result page is displayed")
            return True

        except PlaywrightTimeoutError:
            logger.error("Chart result page is not displayed")
            return False


