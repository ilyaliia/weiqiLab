from pydantic import BaseModel, EmailStr

from typing import Optional

import datetime


class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr

    # Profile
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    language: str = "ru"

    # Game
    rating: int = 0  # ELO
    games_played: int = 0
    games_won_in_row: int = 0
    win_rate: float = 0.0

    # system
    created_at: datetime
    last_seen: datetime
    is_online: bool = True

