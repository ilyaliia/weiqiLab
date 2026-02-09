from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os

from models.books import Books
from schemas.books.books import BookSchema, BookSearchFilter
from database import get_session

router = APIRouter()
os.makedirs("uploads/books", exist_ok=True)


@router.get(
    "/books",
    response_model=List[BookSchema],
    summary="Get all books",
    description="Returns a list of all available books",
    tags=["Books 📚"]
)
async def get_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Books))
    return result.scalars().all()


# Book wo file
@router.post(
    "/books",
    summary="Create book record",
    description="Creates a book entry without file. Use upload endpoint to add PDF.",
    tags=["Books 📚"]
)
async def create_book(book_data: BookSchema, session: AsyncSession = Depends(get_session)):
    new_book = Books(**book_data.dict())
    session.add(new_book)
    await session.commit()
    return {"id": new_book.id, "message": "Book created, now upload file"}


# Load file to book
@router.post(
    "/books/{book_id}/upload",
    summary="Upload book file",
    description="Uploads PDF file for an existing book record",
    tags=["Books 📚"]
)
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


@router.get(
    "/books/search",
    summary="Search books",
    description="Advanced search for books with filters, pagination and sorting",
    tags=["Books 📚"]
)
async def search_books(
        filter: BookSearchFilter = Depends(),
        session: AsyncSession = Depends(get_session)
):
    query = select(Books)

    filters = []

    if filter.title:
        filters.append(Books.title.ilike(f"%{filter.title}%"))
    if filter.author:
        filters.append(Books.author.ilike(f"%{filter.author}%"))
    if filter.level:
        filters.append(Books.level == filter.level)
    if filter.language:
        filters.append(Books.language == filter.language)

    # Year
    if filter.year:
        filters.append(Books.year == filter.year)
    else:
        if filter.year_from:
            filters.append(Books.year >= filter.year_from)
        if filter.year_to:
            filters.append(Books.year <= filter.year_to)

    # Pages
    if filter.pages_from:
        filters.append(Books.pages >= filter.pages_from)
    if filter.pages_to:
        filters.append(Books.pages <= filter.pages_to)

    # query
    if filters:
        query = query.where(*filters)

    # pagination
    query = query.limit(filter.limit).offset(filter.offset)

    # db search by filter
    result = await session.execute(query)
    books = result.scalars().all()

    return {
        "count": len(books),
        "limit": filter.limit,
        "offset": filter.offset,
        "books": books
    }
