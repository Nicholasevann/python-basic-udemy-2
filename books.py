from fastapi import Body, FastAPI

app = FastAPI()

Books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance"},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Fiction"},
]

@app.get("/")
async def first_api():
    return {"message": "Hello, World!"}

@app.get("/books")
async def get_books():
    return Books

@app.get("/books/mybook")
async def get_my_books():
    return {"message": "List of my books"}

# @app.get("/books/{book_id}")
# async def get_book(book_id: int):
#     return {'id' : book_id}
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in Books:
        if book['title'].lower() == book_title.lower():
            return book
    return {"message": "Book not found"}

@app.get("/books")
async def read_category(category: str):
    books_to_return = []
    for book in Books:
        if book.get('category').lower() == category.lower():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str = None):
    books_to_return = []
    for book in Books:
        if book.get('author').lower() == book_author.lower():
            if category is None or book.get('category').lower() == category.lower():
                books_to_return.append(book)
    return books_to_return

@app.post("/books/create")
async def create_book(book: dict = Body(...)):
    Books.append(book)
    return {"message": "Book created successfully", "book": Books}

@app.put("/books/update/{book_id}")
async def update_book(book_id: int, book: dict = Body(...)):
    for index, existing_book in enumerate(Books):
        if existing_book['id'] == book_id:
            Books[index] = book
            return {"message": "Book updated successfully", "book": book}
    return {"message": "Book not found"}

@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(Books):
        if book['id'] == book_id:
            del Books[index]
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}