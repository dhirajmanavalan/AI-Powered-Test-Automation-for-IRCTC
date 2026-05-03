from playwright.sync_api import Page ,expect
import re
class SearchTrainsPage:

    def __init__(self, page:Page):
        self.page = page

    # LOCATORS
    FROM_BOX = "//input[contains(@aria-label,'From station')]"
    TO_BOX = "//input[contains(@aria-label,'To station')]"
    DATE_BOX = "//span[contains(@class,'ui-calendar')]//input"
    CLASS_BOX = "//div[contains(@class,'ng-tns-c76-10 ui-dropdown')]"
    GENERAL_BOX = "//div[contains(@class,'ng-tns-c76-11 ui-dropdown')]"
    SEARCH_BUTTON = "//button[contains(@class,'search_btn')]"

    def search_trains(self, source:str, destination:str, date:str=None, classes:str=None, general:str=None):
        # FROM
        from_search = self.page.locator(self.FROM_BOX)
        from_search.fill(source)
        #self.page.wait_for_timeout(1000)
        self.page.locator(f"(//span[contains(.,'{source}')])[1]").wait_for(state="visible")

        self.page.locator(f"(//span[contains(.,'{source}')])[1]")
        self.page.keyboard.press("Enter")

        # TO
        to_search = self.page.locator(self.TO_BOX)
        to_search.fill(destination)
        #self.page.wait_for_timeout(1000)
        self.page.locator(f"(//span[contains(.,'{destination}')])[1]").wait_for(state="visible")

        self.page.locator(f"(//span[contains(.,'{destination}')])[1]")
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