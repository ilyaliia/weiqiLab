from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Text
from database import Base


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    year: Mapped[int]
    level: Mapped[str]
    description: Mapped[str]
    language: Mapped[str] = "ru"
    pages: Mapped[int]

    # Сделай поля nullable=True
    file_path: Mapped[str] = mapped_column(nullable=True)
    file_size: Mapped[int] = mapped_column(nullable=True)
    file_format: Mapped[str] = mapped_column(nullable=True)