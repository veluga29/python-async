import asyncio
import aiohttp
import time
import os
import threading


async def fetcher(session, url):
    print(
        f"process id : {os.getpid()} | thread id: {threading.get_ident()} | url: {url}"
    )
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = ["https://google.com", "https://instagram.com"] * 50

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *[fetcher(session, url) for url in urls]
        )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)  # 3
