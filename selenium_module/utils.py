from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import exceptions
from requests.cookies import RequestsCookieJar


def _dicted_cookies(cookies: dict):
    for k, v in cookies.items():
        print('DICTING')
        # todo fix
        try:
            yield {'name': k, 'value': v['value']}
        except ValueError:
            yield {'name': k, 'value': v}


def _wrap_method(driver, cookie_dict):
    try:
        driver.add_cookie(cookie_dict)
        print('ADDED COOKIES')
    except exceptions.InvalidCookieDomainException as e:
        print(e.msg)
    except Exception as e:
        print('ERROR', type(e), e, cookie_dict)


def add_cookies(driver: WebDriver, cookies: 'dict|list|RequestsCookieJar'):
    if isinstance(cookies, RequestsCookieJar):
        cookies = {k: v for k, v in cookies.items()}

    if isinstance(cookies, dict):
        for cookie_dict in _dicted_cookies(cookies):
            _wrap_method(driver, cookie_dict)

    elif isinstance(cookies, list):
        for cookie_set in cookies:
            for cookie_dict in _dicted_cookies(cookie_set):
                _wrap_method(driver, cookie_dict)


def normalize_cookies(cookies_list: list[dict]):
    """
        Function to normalize cookies from selenium
    """
    normalized_cookies = {}
    for cookie in cookies_list:
        normalized_cookies.update({cookie.pop('name'): cookie})
    return normalized_cookies
