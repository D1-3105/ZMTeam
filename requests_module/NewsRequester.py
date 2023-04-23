import requests
from config import request_config


class NewsRequester(requests.Session):
    base_url = 'https://news.google.com'
    proxies: dict  # I've been banned on Google News, so I've got to use proxy now :D

    def __init__(self):
        super().__init__()
        self.adapters.get('https://').max_retries = request_config.https_max_retries
        self.proxies = request_config.proxies

    def request_main_page(self) -> requests.Response:
        """
        Uses proxy to request main page
        """
        return self.get(
            self.base_url + '/home',
            verify=False,
            proxies=self.proxies
        )

    def request_article(self, path: str) -> requests.Response:
        """
        Resolves true url of article. Required, because google bans by ip!
        Status: 301,
        Location in headers leads to source of an article!
        :param path: ./articles/CBMia2h0dHBzOi8vaW5kaWFuZXhwcmVzcy
        :return: Response
        """
        url = path.replace('.', self.base_url)
        return self.get(
            url,
            verify=False,
            proxies=self.proxies,
            allow_redirects=False
        )
