import pytest
from playwright.sync_api import sync_playwright

from pages import HomePage


def accept_cookies(browser_context):
    """Accepts cookies by adding a predefined consent cookie to the browser context.

    It simulates accepting cookies on the website by adding a cookie  that marks the user's consent to the cookie
     policy in the browser context.  This ensures the application behaves as if the user has accepted the policy.

    param browser instance browser_context: The browser context where the cookie should be added.
    """
    browser_context.add_cookies([
            {
                'name': '__kwc_agreed',
                'value': 'true',
                'domain': 'www.kiwi.com',
                'path': '/',
                'httpOnly': False,
                'secure': True
            }
        ])


@pytest.fixture(scope='session')
def browser():
    """Provides a browser page instance for tests with cookies pre-accepted.

    @param string session: The browser instance is shared across all tests in the session.
    @yield browser instance Page: A Playwright page object for interacting with the browser during tests.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        browser_context = browser.new_context()
        accept_cookies(browser_context)

        yield browser_context.new_page()

        browser.close()


@pytest.fixture
def page_factory(browser):
    """ Provides a factory function to initialize and return page objects for tests.

    This fixture creates page objects dynamically based on the provided class name.
    Page objects are initialized only when they are accessed for the first time.

    @param object browser: The browser context used to initialize page objects.

    @return Callable: A function that takes a page name as a string (e.g., 'home_page')  and returns the corresponding
    page object, creating it only when needed.
    """

    class LazyPageFactory:
        def __init__(self, browser):
            self.browser = browser
            self.pages = {}

        def get_page(self, class_name):
            page_classes = {
                'home_page': HomePage
            }
            if class_name not in page_classes:
                raise ValueError(f'Page class "{class_name}" is not defined in LazyPageFactory.')

            if class_name not in self.pages:
                self.pages[class_name] = page_classes[class_name](self.browser)

            return self.pages[class_name]

    factory = LazyPageFactory(browser)
    return factory.get_page