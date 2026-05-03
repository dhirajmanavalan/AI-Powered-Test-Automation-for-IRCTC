from playwright.sync_api import Page

class TicketCancelHistoryPage:
    # LOCATORS
    ACCOUNT = "//a[contains(.,'MY ACCOUNT')]"
    TRANSACTIONS = "//span[text()='My Transactions']"
    CANCELLATION_HISTORY = "// span[text()= 'Ticket Cancellation History']"

    def __init__(self, page: Page):
        self.page = page

    def go_to_ticket_cancellation_history(self):
        # Step 1: Click MY ACCOUNT
        my_account = self.page.locator(self.ACCOUNT)
        my_account.wait_for(state="visible")
        my_account.click()

        # Step 2: Hover My Transactions
        my_transactions = self.page.locator(self.TRANSACTIONS)
        my_transactions.wait_for(state="visible")
        my_transactions.hover()

        # Step 3: Click Ticket Cancellation History
        cancellation = self.page.locator(self.CANCELLATION_HISTORY)
        cancellation.wait_for(state="visible")
        cancellation.click()