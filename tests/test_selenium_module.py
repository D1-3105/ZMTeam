import pytest
import random
from .fixtures import urls, browser, news_ses
from selenium.webdriver.remote.webdriver import WebDriver
from requests_module import NewsRequester
from selenium_module.browse import Browser


def test_selenium_browsing(news_ses: NewsRequester, urls, browser: WebDriver):
    news_url: str = random.choice(urls)
    url = news_ses.request_article(news_url).headers.get('Location')
    browser_processor = Browser(browser)
    browser_processor.browse_page(url)
    browser_processor.scroll_down(
        lambda driver: print('COOKIES', driver.get_cookies())
    )

