import random
from requests_module import NewsRequester
from mp_module.processor import PoolExecutor
from requests_module.parsing import ArticleLinkParser
from target import Target

if __name__ == '__main__':

    with NewsRequester() as news_ses:
        resp = news_ses.request_main_page()
    data = resp.content
    url_parser = ArticleLinkParser()
    url_parser.feed(data.decode())
    urls = list(url_parser.articles)
    cookies = news_ses.cookies
    futures = []
    with PoolExecutor(max_processes=5) as pool_executor:
        while urls:
            rand_index = random.randint(0, len(cookies)-1)
            if rand_index >= 0:
                try:
                    url = urls.pop(rand_index)
                except:
                    print(rand_index, urls)
            target = Target(url, cookies)

            future = pool_executor.run(
                target
            )
            futures.append(future)
        results = [f() for f in futures]
        pool_executor._factory.join()

