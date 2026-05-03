from playwright.sync_api import Page
class PassengerDetailsPage:
    def __init__(self, page: Page):
        self.page = page

    NAME_INPUTS = "xpath=//input[@role='searchbox' and @placeholder='Name']"
    AGE_INPUTS = "xpath=//input[@type='number' and @placeholder='Age']"
    GENDER_DROPDOWNS = "xpath=//select[@formcontrolname='passengerGender']"
    BERTH_DROPDOWNS = "xpath=//select[@formcontrolname='passengerBerthChoice']"
    ADD_PASSENGER_BUTTON = "xpath=//span[contains(@class,'prenext') and contains(normalize-space(),'+ Add Passenger')]"
    MOBILE_NUMBER_INPUT = "xpath=//input[@formcontrolname='mobileNumber' and @placeholder='Passenger mobile number *']"

    AUTO_UPGRADE_LABEL = (
        "xpath=//label[@for='autoUpgradation' and "
        "contains(normalize-space(),'Consider for Auto Upgradation')]"
    )

    # radio labels, not inputs
    PAYMENT_CARD_LABEL = (
        "xpath=//label[@for='3'and contains(normalize-space(),'Credit & Debit')]//div[@role='radio']"
    )
    PAYMENT_UPI_LABEL = (
        "xpath=//label[@for='2' and contains(normalize-space(),'BHIM/UPI')]//div[@role='radio']"
    )

    CONTINUE_BUTTON = (
        "xpath=//button[@type='submit' and contains(@class,'train_Search') "
        "and normalize-space()='Continue']"
    )
    # HELPER FUNCTION
    def wait_for_passenger_page(self):
        self.page.locator(self.NAME_INPUTS).first.wait_for(state="visible", timeout=30000)
        self.page.wait_for_timeout(1000)
    # HELPER FUNCTION
    def click_add_passenger(self):
        self.page.locator(self.ADD_PASSENGER_BUTTON).first.click()
        self.page.wait_for_timeout(1500)
    # HELPER FUNCTION
    def fill_single_passenger(self, passenger_index: int, name: str, age: str, gender: str, berth: str):
        name_input = self.page.locator(self.NAME_INPUTS).nth(passenger_index)
        age_input = self.page.locator(self.AGE_INPUTS).nth(passenger_index)
        gender_dropdown = self.page.locator(self.GENDER_DROPDOWNS).nth(passenger_index)
        berth_dropdown = self.page.locator(self.BERTH_DROPDOWNS).nth(passenger_index)

        name_input.wait_for(state="visible", timeout=15000)

        name_input.click()
        name_input.fill(str(name))

        age_input.click()
        age_input.fill(str(age))

        gender_dropdown.select_option(value=str(gender).upper())
        berth_dropdown.select_option(value=str(berth).upper())

        self.page.wait_for_timeout(1000)
    # HELPER FUNCTION
    def set_auto_upgrade(self, auto_upgrade: bool):
        if not auto_upgrade:
            print("Auto upgrade not requested, skipping")
            return

        try:
            label = self.page.locator(self.AUTO_UPGRADE_LABEL).first
            label.click(timeout=5000)
            print("Auto upgrade selected using label click")
            self.page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Auto upgrade label not handled: {e}")
    # HELPER FUNCTION
    def select_payment_mode(self, payment_mode: str):
        payment_mode = payment_mode.strip().lower()

        if payment_mode == "card":
            label = self.page.locator(self.PAYMENT_CARD_LABEL).first
        elif payment_mode == "upi":
            label = self.page.locator(self.PAYMENT_UPI_LABEL).first
        else:
            raise ValueError("payment_mode must be either 'card' or 'upi'")

        label.wait_for(state="visible", timeout=10000)
        label.click(timeout=5000)
        print(f"Payment mode selected via label: {payment_mode}")
        self.page.wait_for_timeout(1000)
    # HELPER FUNCTION
    def click_continue(self):
        self.page.locator(self.CONTINUE_BUTTON).first.click()
        self.page.wait_for_timeout(2000)

    def fill_all_passengers(
        self,
        passengers: list[dict],
        mobile_number: str,
        auto_upgrade: bool = False,
        payment_mode: str = "card",
    ):
        self.wait_for_passenger_page()

        for index, passenger in enumerate(passengers):
            if index > 0:
                self.click_add_passenger()

            self.fill_single_passenger(
                passenger_index=index,
                name=passenger["name"],
                age=passenger["age"],
                gender=passenger["gender"],
                berth=passenger["berth"],
            )

        mobile_input = self.page.locator(self.MOBILE_NUMBER_INPUT).first
        mobile_input.click()
        mobile_input.fill(str(mobile_number))
        self.page.wait_for_timeout(1000)

        self.set_auto_upgrade(auto_upgrade)
        self.select_payment_mode(payment_mode)
        self.click_continue()