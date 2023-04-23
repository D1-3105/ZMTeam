import os

import pytest
from requests_module import NewsRequester
from requests_module.parsing import ArticleLinkParser
from selenium_module.browse import DriverFactory
from config.selenium_config import BROWSER
from config import db_config
from config import BASE_PATH
from db.utils import MigrationExecutor, ConnectionFactory


@pytest.fixture(scope='session')
def news_ses():
    with NewsRequester() as ses:
        yield ses


@pytest.fixture
def urls(news_ses):
    resp = news_ses.request_main_page()
    data = resp.content
    url_parser = ArticleLinkParser()
    url_parser.feed(data.decode())
    return list(url_parser.articles)


@pytest.fixture(scope='session')
def browser():
    factory = DriverFactory(**BROWSER)
    yield factory.browser
    factory.browser.close()


@pytest.fixture
def db():
    db_config.DATABASE['name'] = 'TEST_DB.sqlite3'
    MigrationExecutor().run()
    connection = ConnectionFactory()
    yield connection.db
    connection.db.close()
    os.remove(BASE_PATH / db_config.DATABASE['name'])
