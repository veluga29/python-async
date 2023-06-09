import requests
import time


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


def main():
    urls = [
        "https://naver.com",
        "https://google.com",
        "https://instagram.com",
    ] * 10

    with requests.session() as session:
        results = [fetcher(session, url) for url in urls]
        print(results)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"총 소요시간: {end - start}시간")
