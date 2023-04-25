from selenium_module.browse import Browser, DriverFactory
from requests_module.NewsRequester import NewsRequester
from selenium_module.utils import add_cookies
from selenium_module.browse import retrieve_normalized_cookies, WebDriver
from db.db_processor import CookieHandler
from config.selenium_config import BROWSER
from requests.cookies import RequestsCookieJar

import urllib3.exceptions

from typing import Any

import logging

logger = logging.getLogger(__name__)


class Target:
    """
        In-Pool executive target
    """
    _cookies: 'Any'
    _news_requester: 'NewsRequester | None' = None
    _driver: 'WebDriver | None' = None
    _browser: 'Browser | None' = None
    _cookie_handler: 'CookieHandler | None' = None
    url: 'str|None' = None

    @property
    def news_requester(self):
        if not self._news_requester:
            self._news_requester = NewsRequester()
        return self._news_requester

    @property
    def driver(self):
        if not self._driver:
            factory = DriverFactory(**BROWSER)
            self._driver = factory.browser
        return self._driver

    @property
    def browser(self):
        """
            Lazy initialization of Browser based on current webdriver
        """
        if not self._browser:
            self._browser = Browser(self.driver)
        return self._browser

    def __init__(
            self,
            google_url,
            initial_cookies: RequestsCookieJar
    ):
        self.url = google_url
        self._initial_cookies = {k: v for k, v in initial_cookies.iteritems()}

    def __call__(self):
        """
            1. Resolves actual url via proxy
            2. Fetches cookies from db, updates initial cookies, passes em to driver
            3. Gets page
            4. Scrolls down, applies success callback
        """
        actual_url = self.resolve_link(self.url)
        self._cookie_handler = CookieHandler(actual_url)
        print('HANDLER READY')
        cookies = self._initial_cookies
        cookies.update(self._cookie_handler.initial)
        print('INITIAL COOKIES', self._initial_cookies)
        self.url = actual_url
        print('BROWSING PAGE')
        self.browser.browse_page(actual_url, self._initial_cookies)
        print('SCROLL PAGE DOWN')
        self.browser.scroll_down(self.success_callback)
        # add callback to close

    def __del__(self):
        self.close()

    def success_callback(self, driver: WebDriver):
        """
        Normalizes cookies and saves them to db
        :param driver: Driver passed from browser
        :return:
        """
        cookies = retrieve_normalized_cookies(driver)
        self._cookie_handler(cookies)

    def close(self):
        if self._news_requester:
            self._news_requester.close()
        if self._driver:
            try:
                self._driver.quit()
            except urllib3.exceptions.MaxRetryError as e:
                print(e)
        if self._cookie_handler:
            self._cookie_handler.close()

    def resolve_link(self, google_url: str):
        """
            Resolves google redirect-url into real source url
        """
        print('RESOLVING URL')
        url_response = self.news_requester.request_article(google_url)
        actual_url = url_response.headers.get('Location')
        print('RESOLVED URL', actual_url)
        return actual_url


