from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()


templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터 북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str | None = None):
    keyword = q
    if not keyword:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "title": "콜렉터 북북이"},
        )
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(
            BookModel, BookModel.keyword == keyword
        )
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "콜렉터 북북이",
                "keyword": q,
                "books": books,
            },
        )

    scraper = NaverBookScraper()
    books = await scraper.search(keyword, 10)
    book_models = [
        BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["discount"],
            image=book["image"],
        )
        for book in books
    ]
    await mongodb.engine.save_all(book_models)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "콜렉터 북북이", "keyword": q, "books": books},
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()
