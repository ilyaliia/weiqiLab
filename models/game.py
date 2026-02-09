from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, Enum, Float, DateTime
from database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    board_size = Column(Integer, default=19)
    handicap = Column(Integer, default=0)
    komi = Column(Float, default=6.5)
    bot_rating = Column(Integer, default=1000)

    user_is_black = Column(Boolean, default=True)
    opponent_type = Column(String, default="bot")
    current_player = Column(Integer, default=1)  # 1=black, 2=white

    grid = Column(JSON, default=lambda: [[0] * 19 for _ in range(19)], nullable=False)

    black_captured = Column(Integer, default=0)
    white_captured = Column(Integer, default=0)

    status = Column(String, default="active")  # active, finished, resigned

    last_grid_hash = Column(String, nullable=True) # ko
    created_at = Column(DateTime, default=datetime.utcnow)
