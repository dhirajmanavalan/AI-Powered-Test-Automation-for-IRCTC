import pytest
import allure
from pages.login_page import LoginPage
from pages.search_train_page import SearchTrainsPage
from pages.booking_page import BookingPage
from pages.passenger_details_page import PassengerDetailsPage


@allure.feature("IRCTC Booking Flow")
@allure.story("Passenger Details Submission")
@allure.title("Verify passenger details submission during ticket booking")
@allure.description(
    "This test verifies that passenger details are correctly filled and submitted during the IRCTC ticket booking flow. "
    "It covers login, train search, train selection, and passenger details submission."
)
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.booking
class TestPassengerDetails:
    def test_passenger_details_submission(
        self, page
    ) -> None:
        """
        Test Case: Verify passenger details submission during ticket booking.
        
        Steps:
        1. Login to IRCTC with valid credentials.
        2. Search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026.
        3. Select a train with available seats in SL class.
        4. Fill passenger details and submit.
        """
        # Initialize Page Objects
        login_page = LoginPage(page)
        search_page = SearchTrainsPage(page)
        booking_page = BookingPage(page)
        passenger_page = PassengerDetailsPage(page)

        # Step 1: Load IRCTC home page and login
        with allure.step("Load IRCTC home page and login with credentials"):
            login_page.load_login_page()
            login_page.login("Dhiru_naughty", "DhirDhir@12")
            assert login_page.login_status("Dhiru_naughty"), "Login failed"

        # Step 2: Search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026
        with allure.step(
            "Search for trains from Chennai (MS) to Bangalore (SBC) on 28/05/2026"
        ):
            search_page.search_trains(
                source="CBE",
                destination="ED",
                date="26/06/2026",
                classes="SL",
                general=None,
            )
            assert search_page.is_search_results_displayed(), "Train search results not displayed"

        # Step 3: Select a train with available seats in SL class
        with allure.step(
            "Select a train with available seats in SL class for 28/05/2026"
        ):
            booking_page.select_train_based_on_availability(
                input_date="26/06/2026", preferred_class="SL"
            )

        # Step 4: Fill passenger details and submit
        with allure.step("Fill passenger details and submit"):
            passenger_page.fill_all_passengers(
                passengers=[
                    {"name": "DHIRAJKUMAR M", "age": "22", "gender": "M", "berth": "SL"},
                    {"name": "Debdeepta S.", "age":"22","gender": "M", "berth": "SL"}
                ],
                mobile_number="8489403967",
                auto_upgrade=True,
                payment_mode="card",
            )