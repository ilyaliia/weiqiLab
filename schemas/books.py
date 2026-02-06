from pydantic import BaseModel


class BookSchema(BaseModel):
    title: str
    author: str
    year: int
    level: str
    description: str
    language: str = "ru"
    pages: int
