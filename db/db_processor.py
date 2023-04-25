import json
from datetime import datetime
from .utils import QueryExecutor, ConnectionFactory
from .crud import (
    select_profile_query,
    create_profile_query,
    update_profile_query
)
from urllib.parse import urlparse


class CookieHandler:

    def __init__(self, url, con_factory=None):
        self._con_fact = con_factory or ConnectionFactory()
        self.executor = QueryExecutor(self._con_fact.db)
        url = urlparse(url)
        self.domain = url.netloc

    def get_by_domain(self, *fields):
        select = select_profile_query(
            self.domain,
            *fields
        )
        self.executor.add_query(select)
        return self.executor.run()

    @property
    def initial(self) -> dict:
        """
            :return: Dumped cookies from db for current domain
        """
        print('OBTAINING INITIAL COOKIES')
        fetched = self.get_by_domain('cookie_val')
        if fetched:
            print(fetched)
            cookie = fetched.pop()[0]
            cookie = json.loads(cookie)
        else:
            cookie = {}
        print('INITIAL VALUES OBTAINED', cookie)
        return cookie

    def __call__(self, cookies):
        """
            :param cookies: cookies as {"name": "value"} dict
            :return: None
        """
        if not cookies:
            return
        cookies = json.dumps(cookies)
        current_values = self.get_by_domain('exec_num')
        if current_values:
            exec_num = current_values[0][0]
            query = update_profile_query(
                cookie_val=cookies,
                id=self.domain,
                dt_execution=datetime.now(),
                exec_num=exec_num + 1
            )
        else:
            query = create_profile_query(
                cookie_val=cookies,
                id=self.domain,
                dt_execution=datetime.now(),
                exec_num=1
            )
        self.executor.add_query(query)
        self.executor.run()
        self.executor.do_commit()

    def __del__(self):
        self.executor.close()

    def close(self):
        self.executor.close()
