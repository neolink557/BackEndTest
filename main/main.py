import os
from fastapi import FastAPI
import sqlalchemy
import uvicorn
import databases

DATABASE_URL = os.getenv("DATABASE_URL")

if "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Example endpoint to fetch all books
@app.get("/books")
async def get_books():
    query = "SELECT * FROM books"
    return await database.fetch_all(query=query)

# NEW ENDPOINT: Get all books for a specific author
@app.get("/authors/{author_id}/books")
async def get_books_by_author(author_id: int):
    query = "SELECT * FROM books WHERE author_id = :author_id"
    return await database.fetch_all(query=query, values={"author_id": author_id}) 


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)