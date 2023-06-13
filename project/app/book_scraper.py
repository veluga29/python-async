import aiohttp
from app.config import NAVER_API_ID, NAVER_API_SECRET


class BookScraper:
    def __init__(self):
        pass

    async def fetch(self, session: aiohttp.ClientSession, url: str):
        headers = {
            "X-Naver-Client-Id": NAVER_API_ID,
            "X-Naver-Client-Secret": NAVER_API_SECRET,
        }

        async with session.get(url, headers=headers) as response:
            return await response.json()


book_scraper = BookScraper()
