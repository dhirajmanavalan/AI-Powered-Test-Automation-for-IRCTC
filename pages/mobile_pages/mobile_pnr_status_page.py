from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from utils.logger import get_logger


logger = get_logger()


class MobilePNRStatusPage:
    def __init__(self, mobile_page: Page):
        self.page = mobile_page
        self.context = mobile_page.context
        self.pnr_page: Page | None = None

    # LOCATORS
    PNR_BUTTON = "(//label[contains(@class,'search_btn') and normalize-space()='PNR STATUS'])[2]"
    PNR_NUMBER = "//input[@id='inputPnrNo']"
    INITIAL_SUBMIT_BUTTON = "//input[@id='modal1']"
    CAPTCHA_SUBMIT_BUTTON = "input#submitPnrNo"
    NOTIFICATION_POP_UP = "//button[contains(text(), 'Later')]"

    # HELPER FUNCTION
    def wait_for_manual_captcha_submit(self, pnr_page: Page) -> None:
        """
        Waits for user to manually enter CAPTCHA and click submit button.

        Important:
        This must run on the new PNR tab, not on the original page.
        """

        try:
            # Wait for CAPTCHA submit button to exist in the new tab
            pnr_page.wait_for_selector(
                self.CAPTCHA_SUBMIT_BUTTON,
                state="attached",
                timeout=30000
            )

            # Inject listener in the new tab
            pnr_page.evaluate(
                """
                const btn = document.querySelector('input#submitPnrNo');

                if (!btn) {
                    throw new Error('CAPTCHA submit button not found');
                }

                window.manualStepDone = false;

                btn.addEventListener('click', () => {
                    window.manualStepDone = true;
                }, { once: true });
                """
            )

            print("\nWaiting for manual CAPTCHA entry and submit click...")
            print("Enter CAPTCHA manually on the website, then click Submit.")
            logger.info("Waiting for manual CAPTCHA submit click")

            # Wait up to 2 minutes for manual click
            pnr_page.wait_for_function(
                "window.manualStepDone === true",
                timeout=120000
            )

            print("Click detected! Continuing script...")
            logger.success("Manual CAPTCHA submit click detected")

            # Give result page/state a moment to update
            pnr_page.wait_for_load_state("domcontentloaded", timeout=30000)

        except PlaywrightTimeoutError:
            logger.exception(
                "Timed out waiting for manual CAPTCHA submit click. "
                "Make sure CAPTCHA is entered and Submit is clicked manually."
            )
            raise

        except Exception as error:
            logger.exception(f"Manual CAPTCHA handling failed: {error}")
            raise

    def pnr_status(self, pnr_number: str) -> None:
        """
        Opens PNR status page in a new tab, enters PNR number,
        waits for manual CAPTCHA entry, and continues after manual submit click.
        """

        if not pnr_number:
            raise ValueError("PNR number is required")

        logger.info(f"Starting PNR status flow for PNR: {pnr_number}")

        try:
            self.page.locator(self.NOTIFICATION_POP_UP).wait_for(state="visible")
            self.page.locator(self.NOTIFICATION_POP_UP).click()
        except TimeoutError:
            print("Notification didn't pop up")

        try:
            # Step 1: Click PNR STATUS and capture the new tab
            with self.context.expect_page() as new_page_info:
                self.page.locator(self.PNR_BUTTON).click()

            new_tab = new_page_info.value
            self.pnr_page = new_tab

            new_tab.wait_for_load_state("domcontentloaded", timeout=60000)

            logger.info(f"PNR page title: {new_tab.title()}")
            print(new_tab.title())

            # Step 2: Enter PNR number in the new tab
            pnr_input = new_tab.locator(self.PNR_NUMBER)
            expect(pnr_input).to_be_visible(timeout=30000)
            pnr_input.fill(pnr_number)

            logger.info("PNR number entered successfully")

            # Step 3: Click initial submit button to show CAPTCHA
            initial_submit = new_tab.locator(self.INITIAL_SUBMIT_BUTTON)
            expect(initial_submit).to_be_visible(timeout=30000)
            initial_submit.click()

            logger.info("Initial PNR submit clicked. Waiting for CAPTCHA submit button.")

            # Step 4: Handle manual CAPTCHA submit on the new tab
            self.wait_for_manual_captcha_submit(new_tab)

        except Exception as error:
            logger.exception(f"PNR status flow failed: {error}")
            raise



    def is_pnr_status_displayed(self, pnr_number: str) -> bool:
        """
        Checks whether PNR status result is displayed.

        Returns:
            True if PNR result is visible.
            False otherwise.
        """

        if self.pnr_page is None:
            logger.error("PNR page is not available. Call pnr_status() first.")
            return False

        pnr_status_visible_text = (
            f"//h4[contains(text(), 'You Queried For : PNR Number: {pnr_number}')]"
        )

        try:
            self.pnr_page.wait_for_url(
                "**/enquiry/PNR/PnrEnquiry**",
                timeout=30000
            )

            expect(
                self.pnr_page.locator(pnr_status_visible_text)
            ).to_be_visible(timeout=30000)

            logger.success("PNR status result is displayed")
            return True

        except Exception as error:
            logger.error(f"PNR status result is not displayed: {error}")
            return False
