import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")

# Construir la URL con sslmode=require si es necesario
if "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

database = Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conectar antes de iniciar la app
    await database.connect()
    yield
    # Desconectar al cerrar la app
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "App con Supabase funcionando correctamente"}

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