from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Friends(Base):
    __tablename__ = "friends"

    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    receiver_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
