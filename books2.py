from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Define Book using Pydantic
class Book(BaseModel):
    id:   Optional[int] = None
    title: str = Field(..., max_length=100)
    author: str 
    description: str
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")

# Sample data
BOOKS = [
    Book(id=1, title="Computer Science Distilled", author="Wladston Ferreira Filho", description="A brief introduction to the fundamentals of computer science.", rating=5),
    Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt and David Thomas", description="A guide to becoming a more effective and pragmatic programmer.", rating=4),
    Book(id=3, title="Clean Code", author="Robert C. Martin", description="A handbook of agile software craftsmanship.", rating=5),
    Book(id=4, title="Design Patterns", author="Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides", description="Elements of reusable object-oriented software.", rating=4),
    Book(id=5, title="Refactoring", author="Martin Fowler", description="Improving the design of existing code.", rating=5),
]

@app.get("/books")
async def get_books():
    return BOOKS

@app.post("/create-book")
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