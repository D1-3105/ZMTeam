from html.parser import HTMLParser


class ArticleLinkParser(HTMLParser):

    """
    Honestly, I would parse this page using BeautifulSoup.
    But requirements are too strict (no module described in a task!)
    """

    articles = set()

    @staticmethod
    def get_attr(attr: str, attrs: list[tuple]):
        for klass, value in attrs:
            if klass == attr:
                return value

    def handle_starttag(self, tag: str, attrs: 'list[tuple[str, str | None]]') -> None:
        if tag == 'a' and (href:=self.get_attr('href', attrs)):
            if href.startswith('./articles/'):
                self.articles.add(href)

