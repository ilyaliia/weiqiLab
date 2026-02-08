from datetime import datetime

from sqlalchemy import ForeignKey, Float, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

from typing import Optional


class Game(Base):
    __tablename__ = "games"

    # from schema
    id: Mapped[int] = mapped_column(primary_key=True)
    board_size: Mapped[int] = mapped_column(Integer, default=19)
    bot_rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    handicap: Mapped[int] = mapped_column(Integer, default=0)
    komi: Mapped[float] = mapped_column(Float, default=6.5)

    # players
    black_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    white_player_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)

    # system
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

