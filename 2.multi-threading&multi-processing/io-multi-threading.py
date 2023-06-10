import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor


def fetcher(params):
    session, url = params
    print(
        f"process id : {os.getpid()} | thread id: {threading.get_ident()} | url: {url}"
    )
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://google.com", "https://instagram.com"] * 50
    executor = ThreadPoolExecutor(max_workers=10)

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        results = list(executor.map(fetcher, params))


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 4
