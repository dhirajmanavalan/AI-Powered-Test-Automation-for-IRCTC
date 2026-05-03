from playwright.sync_api import Page ,expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import re
from utils.logger import get_logger

logger = get_logger()

class MobileSearchTrainsPage:

    def __init__(self, mobile_page:Page):
        self.page = mobile_page

    # LOCATORS
    FROM_BOX = "//input[contains(@aria-label,'From station')]"
    TO_BOX = "//input[contains(@aria-label,'To station')]"
    DATE_BOX = "//span[contains(@class,'ui-calendar')]//input"
    CLASS_BOX = "//div[contains(@class,'ng-tns-c76-10 ui-dropdown')]"
    GENERAL_BOX = "//div[contains(@class,'ng-tns-c76-11 ui-dropdown')]"
    SEARCH_BUTTON = "//button[contains(@class,'search_btn')]"

    NO_DIRECT_TRAIN_POP_UP = "//span[(text()='Yes') and (@class='ui-button-text ui-clickable')]"

    def search_trains(self, source:str, destination:str, date:str=None, classes:str=None, general:str=None):
        # FROM
        from_search = self.page.locator(self.FROM_BOX)
        from_search.fill(source)
        self.page.locator(f"//li[@id='p-highlighted-option']//span[contains(., '{source.upper()}')]").wait_for(state="visible")
        self.page.keyboard.press("Enter")

        # TO
        to_search = self.page.locator(self.TO_BOX)
        to_search.fill(destination)
        self.page.locator(f"//li[@id='p-highlighted-option']//span[contains(., '{destination.upper()}')]").wait_for(state="visible")
        self.page.keyboard.press("Enter")

        #DATE
        if date:
            day = int(date.split("/")[0])
            self.page.locator(self.DATE_BOX).click()
            self.page.locator("//div[contains(@class,'ui-datepicker-group')]").wait_for(state="visible")
            #self.page.wait_for_timeout(1000)
            self.page.locator(f"//a[text()='{day}']").click()

        #CLASSES
        if classes:
            self.page.locator(self.CLASS_BOX).click()
            #self.page.wait_for_timeout(1000)
            self.page.locator(f"(//li[@role='option' and contains(@aria-label,'{classes}')])[1]").wait_for(state="visible")
            self.page.locator(f"(//li[@role='option' and contains(@aria-label,'{classes}')])[1]").click()

        #GENERAL
        if general:
            self.page.locator(self.GENERAL_BOX).click()
            #self.page.wait_for_timeout(1000)
            self.page.locator(f"(//li[@role='option' and contains(@aria-label,'{general}')])[1]").wait_for(state="visible")
            self.page.locator(f"(//li[@role='option' and contains(@aria-label,'{general}')])[1]").click()

        #SEARCH
        #self.page.wait_for_timeout(1000)
        self.page.locator(self.SEARCH_BUTTON).click()

        try:
            self.page.locator(self.NO_DIRECT_TRAIN_POP_UP).wait_for(state="visible",timeout=2000)
            self.page.locator(self.NO_DIRECT_TRAIN_POP_UP).click()
        except PlaywrightTimeoutError:
            logger.info("Not a In-Direct train or pop up is not visible")


    def is_search_results_displayed(self):
        """
           Checks whether the train search result page is displayed.

           Returns:
               True if the current URL matches the train-list page.
               False otherwise.
           """

        try:
            self.page.wait_for_url("**/booking/train-list**")

            expect(self.page).to_have_url(
                re.compile(r".*/booking/train-list.*"))

            return True

        except Exception:
            return False