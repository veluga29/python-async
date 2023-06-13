from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
import aiohttp
from app.book_scraper import book_scraper


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()


templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(
        keyword="python", publisher="한빛미디어", price=25000, image="python.jpg"
    )
    print(await mongodb.engine.save(book))
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터 북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    BASE_URL = "https://openapi.naver.com/v1/search/book.json"
    urls = [
        f"{BASE_URL}?query={q}&display=20&start={i * 20 + 1}"
        for i in range(10)
    ]

    async with aiohttp.ClientSession() as session:
        data = [await book_scraper.fetch(session, url) for url in urls]

    print(data)
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터 북북이", "keyword": q}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()
