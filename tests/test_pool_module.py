from mp_module.processor import PoolExecutor
from requests_module.parsing import ArticleLinkParser
from main.target import Target
from .fixtures import news_ses

import random


def test_start_one_browser(news_ses):
    resp = news_ses.request_main_page()
    data = resp.content
    url_parser = ArticleLinkParser()
    url_parser.feed(data.decode())
    urls = list(url_parser.articles)
    cookies = news_ses.cookies
    target = Target(random.choice(urls), cookies)
    with PoolExecutor(max_processes=2) as pool_executor:
        future = pool_executor.run(
            target
        )
        print(future)
        print('FUTURE:', future(None))




