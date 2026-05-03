from playwright.sync_api import Page

class MobileLoginPage:
    URL = "https://www.irctc.co.in/nget/train-search"

    def __init__(self, mobile_page :Page):
        self.mobile_page = mobile_page

    #LOCATORS
    IRCTC_LOGIN_LABEL = "// label[text() = 'IRCTC']"
    LOGIN_REGISTER_BUTTON = "//button[contains(text(), 'LOGIN') and contains(text(), 'REGISTER')]"
    USERNAME_INPUT_BOX = "//input[@placeholder='User Name']"
    PASSWORD_INPUT_BOX = "//input[@placeholder='Password']"
    SIGN_IN_BUTTON = "//button[text()='SIGN IN']"
    NOTIFICATION_POP_UP = "//button[contains(text(), 'Later')]"


    def load_login_page(self):
        """
         Load the Login page of IRCTC
        """
        self.mobile_page.goto(MobileLoginPage.URL)

    def login(self, name:str,password:str):
        """
            Logs in to IRCTC using the given username and password.

            This method performs the complete login flow:
            1. Click the IRCTC label to open the collapsable hamburger button
            2. Clicks the Login/Register button.
            3. Locates the username and password input fields.
            4. Clears any existing values from both fields.
            5. Enters the provided username and password.
            6. Clicks the Sign In button to submit the login form.

            Args:
                name (str): The username, email, or mobile number used for login.
                password (str): The password associated with the given user account.

            Returns:
                None
        """

        try:
            self.mobile_page.locator(self.NOTIFICATION_POP_UP).wait_for(state="visible")
            self.mobile_page.locator(self.NOTIFICATION_POP_UP).click()
        except TimeoutError:
            print("Notification didn't pop up")

        self.mobile_page.locator(self.IRCTC_LOGIN_LABEL).click()
        self.mobile_page.locator(self.LOGIN_REGISTER_BUTTON).click()

        user_name = self.mobile_page.locator(self.USERNAME_INPUT_BOX)
        pass_word = self.mobile_page.locator(self.PASSWORD_INPUT_BOX)

        user_name.clear()
        user_name.fill(name)

        pass_word.clear()
        pass_word.fill(password)

        self.mobile_page.click(self.SIGN_IN_BUTTON)

    def login_status(self,name:str)->bool:
        """
        Checks whether the user login was successful.

        Returns:
            bool:
                True if the user is logged in successfully.
                False if the login fails or the logged-in state is not detected.
        """
        LOGGED_IN_USER_NAME = f"//label[contains(text(),'{name}')]"
        self.mobile_page.locator(self.IRCTC_LOGIN_LABEL).click()

        self.mobile_page.locator(LOGGED_IN_USER_NAME).wait_for(state="visible")
        logged_in_user_name = self.mobile_page.locator(LOGGED_IN_USER_NAME)
        return  logged_in_user_name.is_visible()