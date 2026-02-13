# models/puzzles.py
from datetime import datetime
from datetime import date

from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class Puzzles(Base):
    __tablename__ = "puzzles"

    id: Mapped[int] = mapped_column(primary_key=True)
    sgf: Mapped[str] = mapped_column(Text)               # sgf in Text
    difficulty: Mapped[str] = mapped_column(String(10))  # kuy-dan: "15k"
    category: Mapped[str] = mapped_column(String(50))

    author: Mapped[str | None] = mapped_column(String(100), nullable=True)
    source: Mapped[str | None] = mapped_column(String(200), nullable=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)                # count try to answer
    solved: Mapped[int] = mapped_column(Integer, default=0)                  # count right answer


class DailyPuzzle(Base):
    __tablename__ = "daily_puzzles"

    id: Mapped[int] = mapped_column(primary_key=True)
    puzzle_id: Mapped[int] = mapped_column(ForeignKey("puzzles.id"))
    date: Mapped[date] = mapped_column(Date, unique=True)

    puzzle: Mapped["Puzzles"] = relationship()
