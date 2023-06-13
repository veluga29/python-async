import aiohttp
from app.config import NAVER_API_ID, NAVER_API_SECRET
import asyncio


class NaverBookScraper:
    NAVER_API_ID = NAVER_API_ID
    NAVER_API_SECRET = NAVER_API_SECRET
    BASE_URL = "https://openapi.naver.com/v1/search/book.json"

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.BASE_URL}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, i * 10 + 1) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[
                    self.fetch(session, api["url"], api["headers"])
                    for api in apis
                ]
            )
            return [
                book for data in all_data if data is not None for book in data
            ]

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverBookScraper()
    print(scraper.run("파이썬", 3))
    print(len(scraper.run("파이썬", 5)))
