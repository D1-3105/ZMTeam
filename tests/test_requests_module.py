import pytest
from requests_module import NewsRequester
from .fixtures import news_ses
from requests_module.parsing import ArticleLinkParser


def test_news_parse(news_ses):
    ses = news_ses
    resp = ses.request_main_page()
    data = resp.content
    url_parser = ArticleLinkParser()
    url_parser.feed(data.decode())
    print(url_parser.articles)
    assert len(url_parser.articles) != 0
    one_of_articles = url_parser.articles.pop()
    resp = ses.request_article(one_of_articles)
    assert resp.status_code == 301
    assert resp.headers.get('Location') is not None
