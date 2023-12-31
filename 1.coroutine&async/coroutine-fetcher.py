import asyncio
import aiohttp
import time


async def fetcher(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = [
        "https://naver.com",
        "https://google.com",
        "https://instagram.com",
    ] * 10

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetcher(session, url) for url in urls]
        )
        print(results)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"총 소요시간: {end - start}시간")
