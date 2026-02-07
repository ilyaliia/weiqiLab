from pydantic import BaseModel, Field
from typing import Optional


class BookSchema(BaseModel):
    title: str
    author: str
    year: int
    level: str
    description: str
    language: str = "ru"
    pages: int


class BookSearchFilter(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    level: Optional[str] = None
    language: Optional[str] = None

    year: Optional[int] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None

    pages_from: Optional[int] = None
    pages_to: Optional[int] = None

    limit: int = 50
    offset: int = 0
