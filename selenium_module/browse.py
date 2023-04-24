import random
import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from .utils import normalize_cookies, add_cookies

from config.selenium_config import options
from typing import Callable
from .utils import add_cookies
import inspect


class DriverFactory:
    _browser: WebDriver = None

    def __init__(self, browser_type: str, cookies: 'dict | list' = None):
        self.browser = browser_type
        add_cookies(self.browser, cookies)

    @property
    def browser(self):
        """
        Property to get created browser
        """
        return self._browser

    @browser.setter
    def browser(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f'String required, but received: {type(value)}')
        if value == 'Chrome':
            self._browser = webdriver.Chrome(chrome_options=options)
        elif value == 'Firefox':
            self._browser = webdriver.Firefox(options=options)
        else:
            raise ValueError('Unsupported browser!')


def secure(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except WebDriverException as e:

            print(e.msg)
        except Exception as e:
            if inspect.ismethod(func):
                func[0].close()
            print('ERROR', e)
            raise e

    return wrapper


class Browser:
    _driver: WebDriver = None

    def __init__(self, driver: WebDriver):
        if isinstance(driver, WebDriver):
            self._driver = driver
        else:
            raise TypeError(f'WebDriver required, received: {type(driver)}')

    def close(self):
        self._driver.quit()
        self._driver.close()

    def browse_page(self, url: str, cookies):
        print(url)
        url = url.encode('ascii', 'ignore').decode('unicode_escape')
        self._driver.get(url)
        try:
            add_cookies(self._driver, cookies)
        except Exception as e:
            print(e)

    def seek_start(self):
        return self._driver.find_element(By.TAG_NAME, 'body')

    @secure
    def scroll_down(
            self,
            callback_execute: Callable[[WebDriver], None] = None
    ):
        cur_pos = 0
        for i in range(10):  # sometimes there are infinite pages
            print('CURPOS', cur_pos)
            self._driver.execute_script(f'window.scrollTo(0, document.documentElement.scrollHeight - 100)')

            if (new_pos := get_scroll_pos(self._driver)) == cur_pos:
                print('CURPOS', new_pos)
                time.sleep(random.uniform(4, 5))
                break
            else:
                cur_pos = new_pos
                time.sleep(random.uniform(4, 5))

        if callback_execute:
            callback_execute(self._driver)


def retrieve_normalized_cookies(web_driver: WebDriver) -> dict:
    return normalize_cookies(web_driver.get_cookies())


def get_scroll_pos(web_driver: WebDriver) -> int:
    result = web_driver.execute_script('return window.scrollY;')
    return result
