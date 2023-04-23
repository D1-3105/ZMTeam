import random
import time

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from config.selenium_config import options
from typing import Callable


class DriverFactory:
    _browser: WebDriver = None

    def __init__(self, browser_type: str, cookies: dict = None):
        if isinstance(browser_type, str):
            self.browser = browser_type
            if cookies:
                self._browser.add_cookie(cookie_dict=cookies)
        else:
            raise TypeError(f'{type(browser_type) = }')

    @property
    def browser(self):
        """
        Property to get created browser
        """
        return self._browser

    @browser.setter
    def browser(self, value: str):

        if value == 'Chrome':
            self._browser = webdriver.Chrome(options=options)
        elif value == 'Firefox':
            self._browser = webdriver.Firefox(options=options)
        else:
            raise ValueError('Unsupported browser!')


class Browser:
    _driver: WebDriver = None

    def __init__(self, driver: WebDriver):
        if isinstance(driver, WebDriver):
            self._driver = driver
        else:
            raise TypeError(f'WebDriver required, received: {type(driver)}')

    def browse_page(self, url: str):
        print(url)
        url = url.encode('ascii', 'ignore').decode('unicode_escape')
        self._driver.get(url)

    def seek_start(self):
        return self._driver.find_element(By.TAG_NAME, 'body')

    def scroll_down(
            self,
            callback_execute: Callable[[WebDriver], None] = None
    ):
        cur_pos = 0
        while True:
            self._driver.execute_script(f'window.scrollTo(0, document.documentElement.scrollHeight)')
            print('POS', cur_pos)
            if (new_pos := get_scroll_pos(self._driver)) == cur_pos:
                break
            else:
                cur_pos = new_pos
            time.sleep(random.uniform(0.1, 1))

        print(cur_pos)

        if callback_execute:
            callback_execute(self._driver)


def retrieve_cookies(web_driver: WebDriver) -> dict:
    return web_driver.get_cookies()


def get_scroll_pos(web_driver: WebDriver) -> int:
    result = web_driver.execute_script('return window.scrollY;')
    return result
