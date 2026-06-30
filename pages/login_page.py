from playwright.sync_api import Page
import tkinter as tk


import os

def get_viewport_size():

    # Railway deployment
    if os.getenv("RAILWAY_ENVIRONMENT"):
        return 1920, 1080

    # Local machine
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.destroy()

        return width, height

    except Exception:
        return 1920, 1080


class LoginPage:

    URL = "https://www.irctc.co.in/nget/train-search"

    def __init__(self, page: Page):
        self.page = page

    # =========================
    # LOCATORS
    # =========================

    ENGLISH_BUTTON = "//button[text()='English']"

    LOGIN_REGISTER_BUTTON = "//a[text()=' LOGIN / REGISTER ']"
    USERNAME_INPUT_BOX = "//input[@placeholder='User Name']"
    PASSWORD_INPUT_BOX = "//input[@placeholder='Password']"
    SIGN_IN_BUTTON = "//button[text()='SIGN IN']"

    # =========================
    # LOAD PAGE
    # =========================

    def load_login_page(self):
        """
        Load IRCTC page and handle language popup.
        """

        width, height = get_viewport_size()

        self.page.set_viewport_size({
            "width": width,
            "height": height
        })

        self.page.goto(
            LoginPage.URL,
            wait_until="domcontentloaded"
        )

        print("IRCTC page opened")

        try:

            print("Waiting for language popup...")

            self.page.wait_for_selector(
                self.ENGLISH_BUTTON,
                timeout=15000
            )

            self.page.locator(
                self.ENGLISH_BUTTON
            ).scroll_into_view_if_needed()

            self.page.wait_for_timeout(2000)

            self.page.locator(
                self.ENGLISH_BUTTON
            ).click(force=True)

            print("English language selected")

            self.page.wait_for_timeout(2000)

        except Exception as error:

            print(
                f"Language popup handling failed: {error}"
            )

    # =========================
    # LOGIN
    # =========================

    def login(
            self,
            name: str,
            password: str
    ):

        self.page.locator(
            self.LOGIN_REGISTER_BUTTON
        ).click()

        user_name = self.page.locator(
            self.USERNAME_INPUT_BOX
        )

        pass_word = self.page.locator(
            self.PASSWORD_INPUT_BOX
        )

        user_name.clear()
        user_name.fill(name)

        pass_word.clear()
        pass_word.fill(password)

        self.page.locator(
            self.SIGN_IN_BUTTON
        ).click()

    # =========================
    # LOGIN STATUS
    # =========================

    def login_status(
            self,
            name: str
    ) -> bool:

        logged_in_user = (
            f"//span[contains(text(), '{name}')]"
        )

        self.page.locator(
            logged_in_user
        ).wait_for(
            state="visible",
            timeout=10000
        )

        return self.page.locator(
            logged_in_user
        ).is_visible()