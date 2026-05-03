from playwright.sync_api import Page, Locator
from utils.logger import get_logger
import re

logger = get_logger()
class BookingPage:
    def __init__(self, page: Page):
        self.page = page

    TRAIN_CARDS = "xpath=//div[contains(@class,'form-group') and contains(@class,'bull-back') and contains(@class,'border-all')][.//app-train-avl-enq]"
    TRAIN_NAME = "xpath=.//div[contains(@class,'train-heading')]//strong"
    DIMMER = "css=div.dimmer"

    BOOK_NOW_ENABLED = "xpath=.//button[contains(@class,'btnDefault') and normalize-space()='Book Now' and not(contains(@class,'disable-book'))]"

    CONFIRMATION_POPUP = "xpath=//div[contains(@class,'ui-confirmdialog') and .//span[contains(normalize-space(),'Confirmation')]]"
    CONFIRMATION_YES_BUTTON = "xpath=//div[contains(@class,'ui-confirmdialog')]//button[.//span[normalize-space()='Yes']]"

    CLASS_MAP = {
        "SL": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Sleeper') and contains(normalize-space(),'SL')]]",
        "3A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 3 Tier') and contains(normalize-space(),'3A')]]",
        "2A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 2 Tier') and contains(normalize-space(),'2A')]]",
        "1A": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC First Class') and contains(normalize-space(),'1A')]]",
        "3E": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'AC 3 Economy') and contains(normalize-space(),'3E')]]",
        "CC": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Chair Car') and contains(normalize-space(),'CC')]]",
        "EC": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Exec. Chair Car') and contains(normalize-space(),'EC')]]",
        "2S": "xpath=.//div[contains(@class,'white-back') and contains(@class,'col-xs-12')]//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'Second Sitting') and contains(normalize-space(),'2S')]]",
    }
    # HELPER FUNCTION
    def wait_for_results(self):
        try:
            self.page.wait_for_load_state("domcontentloaded")
        except Exception:
            pass

        self.page.locator(self.TRAIN_CARDS).first.wait_for(state="visible", timeout=30000)
        self.page.wait_for_timeout(2000)
    # HELPER FUNCTION
    def _month_abbr(self, input_date: str) -> str:
        month_map = {
            "01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr",
            "05": "May", "06": "Jun", "07": "Jul", "08": "Aug",
            "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"
        }
        return month_map[input_date.split("/")[1]]
    # HELPER FUNCTION
    def _day(self, input_date: str) -> str:
        return str(int(input_date.split("/")[0]))
    # HELPER FUNCTION
    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.strip()).upper()
    # HELPER FUNCTION
    def _is_unavailable(self, status_text: str) -> bool:
        text = self._normalize(status_text)
        return (
            "TRAIN DEPARTED" in text
            or "NOT AVAILABLE" in text
            or "REGRET" in text
        )
    # HELPER FUNCTION
    def _is_bookable(self, status_text: str) -> bool:
        return not self._is_unavailable(status_text)
    # HELPER FUNCTION
    def _wait_for_dimmer_to_disappear(self):
        try:
            self.page.locator(self.DIMMER).wait_for(state="hidden", timeout=5000)
        except Exception:
            pass
    # HELPER FUNCTION
    def _safe_click(self, locator: Locator, name: str):
        self._wait_for_dimmer_to_disappear()

        try:
            locator.scroll_into_view_if_needed(timeout=5000)
        except Exception:
            pass

        try:
            locator.wait_for(state="visible", timeout=10000)
            locator.click(timeout=10000)
            return
        except Exception as e:
            print(f"Normal click failed for {name}: {e}")

        self._wait_for_dimmer_to_disappear()

        try:
            locator.click(timeout=5000, force=True)
            return
        except Exception as e:
            print(f"Force click failed for {name}: {e}")

        self._wait_for_dimmer_to_disappear()

        try:
            locator.evaluate("element => element.click()")
            return
        except Exception as e:
            raise Exception(f"All click methods failed for {name}: {e}")
    # HELPER FUNCTION
    def _get_date_block(self, train_card: Locator, day: str, month_abbr: str) -> Locator:
        return train_card.locator(
            f"xpath=.//td/div[contains(@class,'pre-avl')][.//strong[contains(normalize-space(),'{day}') and contains(normalize-space(),'{month_abbr}')]]"
        )
    # HELPER FUNCTION
    def _get_status_from_date_block(self, date_block: Locator) -> str:
        strongs = date_block.locator("xpath=.//strong")
        count = strongs.count()

        if count >= 2:
            return strongs.nth(1).inner_text().strip()

        return strongs.first.inner_text().strip()
    # HELPER FUNCTION
    def handle_confirmation_popup_if_present(self):
        try:
            popup = self.page.locator(self.CONFIRMATION_POPUP).first
            popup.wait_for(state="visible", timeout=3000)

            yes_button = self.page.locator(self.CONFIRMATION_YES_BUTTON).first
            yes_button.click()

            print(" Confirmation popup appeared, clicked Yes")
            self.page.wait_for_timeout(1500)

        except Exception:
            print("ℹ Confirmation popup did not appear, continuing normally")


    def select_train_based_on_availability(self, input_date: str, preferred_class: str = "SL"):
        self.wait_for_results()

        day = self._day(input_date)
        month_abbr = self._month_abbr(input_date)

        print(f"Looking for date: {day} {month_abbr}")

        train_cards = self.page.locator(self.TRAIN_CARDS)
        total_trains = train_cards.count()
        print(f"Total trains found: {total_trains}")

        for i in range(total_trains):
            try:
                train_card = train_cards.nth(i)

                try:
                    train_card.scroll_into_view_if_needed(timeout=5000)
                except Exception:
                    pass

                train_name = train_card.locator(self.TRAIN_NAME).first.inner_text().strip()
                print(f"Checking Train {i + 1}: {train_name}")

                class_locator = train_card.locator(self.CLASS_MAP[preferred_class])
                class_count = class_locator.count()

                if class_count == 0:
                    print(f"{preferred_class} class not found in {train_name}")
                    continue

                self._safe_click(class_locator.first, f"{preferred_class} class in {train_name}")
                self.page.wait_for_timeout(2000)

                date_block = self._get_date_block(train_card, day, month_abbr)
                date_count = date_block.count()

                if date_count == 0:
                    print(f"Date block not found for {input_date} in {train_name}")
                    continue

                status_text = self._get_status_from_date_block(date_block.first)
                print(f"Status on {input_date}: {status_text}")

                if self._is_unavailable(status_text):
                    print(f"No seats are available in {train_name}")
                    continue

                if self._is_bookable(status_text):
                    print(f"Seat is acceptable in {train_name}. Trying Book Now...")

                    self._safe_click(date_block.first, f"date block in {train_name}")
                    self.page.wait_for_timeout(1500)

                    book_now = train_card.locator(self.BOOK_NOW_ENABLED)
                    book_count = book_now.count()

                    if book_count >= 1:
                        self._safe_click(book_now.first, f"Book Now in {train_name}")
                        print(" Book Now clicked successfully")

                        self.handle_confirmation_popup_if_present()
                        return

                    print(f"Book Now button not enabled in {train_name}")
                    continue

            except Exception as e:
                print(f"Skipping train due to error: {e}")
                continue

        raise AssertionError("No valid train found for selected class and date")