from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os

from models.books import Books
from schemas.books import BookSchema
from database import get_session

router = APIRouter()
os.makedirs("uploads/books", exist_ok=True)


@router.get("/books", response_model=List[BookSchema])
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Books))
    return result.scalars().all()


# Book wo file
@router.post("/books")
async def create_book(book_data: BookSchema, session: AsyncSession = Depends(get_session)):
    new_book = Books(**book_data.dict())
    session.add(new_book)
    await session.commit()
    return {"id": new_book.id, "message": "Book created, now upload file"}


# Load file to book
@router.post("/books/{book_id}/upload")
async def upload_book_file(
        book_id: int,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    # search book by id
    result = await session.execute(select(Books).where(Books.id == book_id))
    book = result.scalar_one()

    # save file
    file_path = f"uploads/books/{book_id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    book.file_path = file_path
    book.file_size = len(content)
    book.file_format = file.filename.split('.')[-1]

    await session.commit()
    return {"message": "File uploaded", "file": file_path}
