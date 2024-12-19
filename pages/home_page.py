import time

from config.urls import BASE_URL
from pages.calendar_page import Calendar

class HomePage:
    """Represents the main page of the application.  It provides methods to interact with and perform actions on the
    home page, such as selecting trip types, setting departure and arrival points, choosing flight dates,
    and managing options like accommodations.
    """

    TRIP_TYPE_DROPDOWN = 'div[data-test*="SearchFormModesPicker"]'
    TRIP_TYPE_OPTION = '//a[contains(@data-test, "ModePopupOption")] //span[text()="%s"]'
    SELECTED_TRIP_TYPE = '(//div[contains(@data-test,"SearchFormModesPicker-active")] //div[text()="%s"])[1]'

    DESTINATION_FIELD_TEMPLATE = '//div[text()="%s"] /ancestor::div[contains(@data-test, "SearchFieldItem")]'
    CLOSE_SELECTED_VALUE_BUTTON = 'div[data-test="PlacePickerInputPlace-close"]'
    SUGGESTION_VALUE = '//div[contains(@data-test, "PlacePickerRow")]'
    FLIGHT_DIRECTION_TEMPLATE = '//div[@data-test="SearchDateInput"] //div[text()="%s"]'
    CALENDAR_DATE_PICKER = 'div[data-test="NewDatePickerOpen"]'
    SUBMIT_SELECTED_DATE = 'button[data-test="SearchFormDoneButton"]'
    BOOKING_ACCOMODATION_CHECKBOX = 'div[data-test="bookingCheckbox"]'
    CHECKED_BOOKING_CHECKBOX = (
        '//div[@data-test="bookingCheckbox"] /label[contains(@class, '
        '"[&_.orbit-checkbox-icon-container]:bg-blue-normal")]'
    )
    SEARCH_BUTTON = 'a[data-test="LandingSearchButton"]'


    def __init__(self, page):
        self.page = page
        self._calendar = None

    def select_trip_type(self, trip_type):
        """Selects the trip type on the homepage. This method converts the provided trip type to match the format used
            on the site (e.g., "one-way" becomes "One-way") and selects it from the dropdown.

        @param string  trip_type: The type of trip to select (e.g., "one-way", "round-trip").
        """
        #convert recieved trip type argument to the value as in on the Site
        trip_type = trip_type.lower().capitalize()

        self.page.click(self.TRIP_TYPE_DROPDOWN)
        self.page.click(self.TRIP_TYPE_OPTION % trip_type)
        self.page.locator(self.SELECTED_TRIP_TYPE % trip_type).wait_for(state='visible')

    def _fill_destination_field(self, field_type: str, field_value: str):
        """ Fills the destination field with the given value.

        @param string field_type: Specifies the type of the field, either "From" (departure) or "To" (arrival).
        @param string  field_value: The value to input into the field.
        """

        locator = self.page.locator(f'{self.DESTINATION_FIELD_TEMPLATE % field_type} //input')
        locator.fill(field_value)

        suggestion_locator = self.page.locator(self.SUGGESTION_VALUE).first
        suggestion_locator.wait_for(state='visible')
        suggestion_locator.click()


    def clear_field_value(self, field='From'):
        """Removes previously entered or default value in 'From' of 'Return' fields

        @param string field: Page field where value should be removed
        """
        field_locator = self.page.locator(self.DESTINATION_FIELD_TEMPLATE % field)
        close_button_locator  = field_locator.locator(self.CLOSE_SELECTED_VALUE_BUTTON)
        close_button_locator.click()


    def set_departure_point(self, departure_value: str, clear_default_value: bool=True):
        """Sets the departure point field with the provided value.

        @param string departure_value: The value to set in the departure field (e.g., airport code like "RTM").
        """
        field_type = 'From'
        if clear_default_value:
            self.clear_field_value(field=field_type)

        self._fill_destination_field(field_type=field_type, field_value=departure_value)

    def set_arrival_point(self, arrival_value: str):
        """ Sets the arrival point field with the provided value.

        @param string arrival_value: The value to set in the arrival field (e.g., airport code like "MAD").
        """

        self._fill_destination_field(field_type='To', field_value=arrival_value)

    @property
    def calendar(self):
        """ Provides access to the Calendar object.

        This property initializes the Calendar object if it has not been created yet
        and returns the instance. It ensures that the Calendar is created only once (lazy initialization).

        @return object Calendar: An instance of the Calendar class for interacting with the calendar component.
        """
        if self._calendar is None:
            self._calendar = Calendar(self.page)
        return self._calendar


    def select_flight_date(self, flight_type: str, time_offset: str):
        """Opens the flight date calendar and selects a date based on time offset.

        @param string flight_type: "Departure" or "Return" to specify which calendar to open.
        @param string time_offset: A string which represents the time offset (ex., '1 week', '3 days', '2 months').
        """

        flight_type = flight_type.lower().capitalize()
        self.page.click(self.FLIGHT_DIRECTION_TEMPLATE % flight_type)
        opened_calendar = self.page.locator(self.CALENDAR_DATE_PICKER)
        opened_calendar.wait_for(state='visible')

        self.calendar.select_offset_time(time_offset)
        self.page.click(self.SUBMIT_SELECTED_DATE)


    def toggle_checkbox(self, action: str):
        """Checks the current state of the checkbox and performs the requested action.
        If the checkbox is already in the desired state, no action is taken.

        @param string action: The desired state for the checkbox. Use "Check" to mark the checkbox or "Uncheck" to
        unmark it.
        """

        action = action.lower().capitalize()
        is_checked = self.page.locator(self.CHECKED_BOOKING_CHECKBOX).count() > 0

        if is_checked and action == 'Uncheck':
            self.page.click(self.BOOKING_ACCOMODATION_CHECKBOX)
        elif not is_checked and action == 'Check':
            self.page.click(self.BOOKING_ACCOMODATION_CHECKBOX)


    def search_execute(self):
        """Executes the search by clicking the search button.

        This method locates the search button on the page, clicks it to start the search,
        and waits until the button is no longer visible, indicating the search is in progress.
        """
        search_button = self.page.locator(self.SEARCH_BUTTON)
        search_button.click()
        search_button.wait_for(state='hidden')



