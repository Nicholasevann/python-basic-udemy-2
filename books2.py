# validate and create a RESTful API using FastAPI
from fastapi import FastAPI, Path, Query, HTTPException
# with Pydantic for data validation and serialization
from pydantic import BaseModel, Field
# to use Optional for optional fields
from typing import Optional
# customize the status code
from starlette import status
app = FastAPI()

# Define Book using Pydantic
class Book(BaseModel):
    id:   Optional[int] = Field(description="ID no need to be provided, it will be auto-generated", default=None)
    title: str = Field(..., max_length=100)
    author: str = Field(..., max_length=100)
    description: str 
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    published_date: int = Field(gt=1900, le=2025, description="Published date must be between 1900 and 2025", default=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Computer Science Distilled",
                "author": "Wladston Ferreira Filho",
                "description": "A brief introduction to the fundamentals of computer science.",
                "rating": 5,
                "published_date": 2025
            }
        }
    }

# Sample data
BOOKS = [
    Book(id=1, title="Computer Science Distilled", author="Wladston Ferreira Filho", description="A brief introduction to the fundamentals of computer science.", rating=5, published_date=2025),
    Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt and David Thomas", description="A guide to becoming a more effective and pragmatic programmer.", rating=4, published_date=2023),
    Book(id=3, title="Clean Code", author="Robert C. Martin", description="A handbook of agile software craftsmanship.", rating=5, published_date=2024),
    Book(id=4, title="Design Patterns", author="Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides", description="Elements of reusable object-oriented software.", rating=4, published_date=2022),
    Book(id=5, title="Refactoring", author="Martin Fowler", description="Improving the design of existing code.", rating=5, published_date=2021),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/",status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, le=5, description="Rating must be between 1 and 5" )):
    books_to_return = []
    rating = int(rating)
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return
 
@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    new_book = Book(**book.model_dump())
    BOOKS.append(find_book_by_id(new_book))
    return {"message": "Book created successfully", "book": BOOKS}


def find_book_by_id(book: Book):
    # more simple way
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    # if(len(BOOKS) > 0):
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    return book

@app.put("/update-book/{book_id}")
async def update_book(book_id: int, book: Book):
    for index, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            updated_book = Book(**book.model_dump())
            updated_book.id = book_id   
            BOOKS[index] = updated_book
            return {"message": "Book updated successfully", "book": updated_book}
        else:
            raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/delete-book/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[index]
            return {"message": "Book deleted successfully","data":BOOKS}
    return {"error": "Book not found"}

@app.get("/books-publish")
async def get_books_by_published_date(published_date: int):
    books_to_return = []
    if 1900 <= published_date <= 2025:
        for book in BOOKS:
            if book.published_date == published_date:
                books_to_return.append(book)
        return books_to_return
    else:
        return {"error": "Published date must be between 1900 and 2025"}