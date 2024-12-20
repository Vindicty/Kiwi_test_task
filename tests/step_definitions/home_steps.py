import re

from pytest_bdd import given, when, then, scenarios, parsers
from playwright.sync_api import expect

from config.urls import SEARCH_RESULTS_URL


@given(
    parsers.cfparse('As an not logged user navigate to homepage {site_url:SiteUrl}', extra_types={'SiteUrl': str})
)
def navigate_to_home_page(page_factory, site_url):
    home_page = page_factory('home_page')
    home_page.page.goto(site_url)
    home_page.page.wait_for_load_state('domcontentloaded')

@when(
    parsers.cfparse('I select {trip_type:TripType} trip type', extra_types={'TripType': str})
)
def select_trip_type(page_factory, trip_type):
    home_page = page_factory('home_page')
    home_page.select_trip_type(trip_type)


@when(
    parsers.cfparse('Set as departure airport {departure_point:DeparturePoint}', extra_types={'DeparturePoint': str})
)
def set_departure_point(page_factory, departure_point):
    home_page = page_factory('home_page')
    home_page.set_departure_point(departure_point)


@when(
    parsers.cfparse('Set as arrival airport {arrival_point:ArrivalPoint}', extra_types={'ArrivalPoint': str})
)
def set_arrival_point(page_factory, arrival_point):
    home_page = page_factory('home_page')
    home_page.set_arrival_point(arrival_point)

@when(
    parsers.cfparse(
        'Set the {flight_type:FlightType} time {time_value:TimeValue} in the future starting current date',
        extra_types={'FlightType': str, 'TimeValue': str}
    )
)
def set_departute_time(page_factory, flight_type: str, time_value: str):
    home_page = page_factory('home_page')
    flight_type = flight_type.lower().capitalize()
    home_page.select_flight_date(flight_type=flight_type, time_offset=time_value)


@when(
    parsers.cfparse(
        '{checkbox_action:CheckboxAction} the `Check accommodation with booking.com` option',
        extra_types={'CheckboxAction': str}
    )
)
def toggle_checkbox(page_factory, checkbox_action):
    home_page = page_factory('home_page')
    home_page.toggle_checkbox(checkbox_action)


@when('Click the search button')
def search_execute(page_factory):
    home_page = page_factory('home_page')
    home_page.search_execute()

@then('I am redirected to search results page')
def is_search_results_opened(page_factory):
    home_page = page_factory('home_page')
    expect(home_page.page).to_have_url(re.compile(r"https://www\.kiwi\.com/en/search/results.*"))
    assert home_page.page.url.startswith(SEARCH_RESULTS_URL), (
        f'Expected URL to start with {SEARCH_RESULTS_URL}, but got {home_page.page.url}'
    )
