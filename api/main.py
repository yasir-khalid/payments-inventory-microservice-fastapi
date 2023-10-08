"""
@author: Yasir Khalid
To simulate CRUD, we would have a list of class objects,
and would append, update, delete and add to the list
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
"""FastAPI runs through the code top to bottom and prioritses API logic based
on the function that appears first
"""


@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: float
    publish_year: int


BOOKS = [
    Book(1, "Apache Spark", "Elon Musk", "Details on Apache spark systems", 4.5, 2009),
    Book(
        2, "Arrow and DuckDB", "Jeff Bezos", "Using DuckDB in modern systems", 4.0, 2022
    ),
    Book(
        3,
        "Imran Khan",
        "PTI Official",
        "Life of Imran Khan and 1992 Worldcup",
        4.7,
        2012,
    ),
    Book(
        4,
        "Mastering AWS and Cloud",
        "Jeff Bezos",
        "AWS cloud infrastructure and cloud " "concepts",
        4.2,
        2015,
    ),
]


@app.get("/")
async def default_landing_zone():
    """Description of the API that shows up in swagger UI"""
    return {"message": "Welcome to my book store"}


@app.get("/books")
async def get_all_books(limit: int = None, rating: float = 0):
    """Using Query params, limit response or filter for ratings"""
    limited_response = BOOKS[:limit] if limit is not None else BOOKS
    return [book for book in limited_response if book.rating >= rating]


@app.get("/books/{book_id}")
async def get_books_by_id(book_id: int):
    """Query books based on ID"""
    return [book for book in BOOKS if book.id == book_id]


@app.get("/books/publish/")
async def get_book_by_publish_year(year: int):
    """Query books based on Publish date"""
    return [book for book in BOOKS if book.publish_year == year]


class BookRequest(BaseModel):
    id: Optional[int] = Field(title="ID is not needed")
    title: str = Field(min_length=3, title="Book Title")
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(ge=0, le=5)
    publish_year: int = Field(ge=1999, le=2031)

    class Config:
        schema_extra = {
            "example": {
                "title": "New book fancy title",
                "author": "Yasir Khalid",
                "description": "new description within 100 characters",
                "rating": 4.0,
                "publish_year": 2009,
            }
        }


@app.post("/create-book")
async def create_new_book(book_request: BookRequest):
    """Create new book, using provided example format"""
    request_to_book_obj = Book(**book_request.dict())
    request_with_newly_attached_id = attach_new_book_id(request_to_book_obj)
    BOOKS.append(request_with_newly_attached_id)
    return {
        "message": "created successfully",
        "timestamp": datetime.now(),
        "data": request_with_newly_attached_id,
    }


def attach_new_book_id(book: Book):
    """Looks at all books in the store, and adds 1 to the last book ID"""
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


class BookUpdateModel(BaseModel):
    id: int = Field(title="Must pass ID related to a book in store")
    title: str = Field(min_length=3, title="Book Title")
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(ge=0, le=5)
    publish_year: int = Field(ge=1999, le=2031)

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "title": "New book fancy title",
                "author": "Yasir Khalid",
                "description": "new description within 100 characters",
                "rating": 4.0,
                "publish_year": 2009,
            }
        }


@app.put("/books/update")
async def update_existing_book(book: BookUpdateModel):
    for i in range(0, len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.dict())
            return {"message": "Book updated", "data": book.dict()}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i in range(0, len(BOOKS)):
        if BOOKS[i].id == book_id:
            _tmp = BOOKS[i]
            BOOKS.pop(i)
            return {"message": "Book deleted successfully", "data": _tmp}
