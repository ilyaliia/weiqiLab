from typing import Literal

from pydantic import BaseModel, Field


class GameCreateSchema(BaseModel):
    board_size: Literal[9, 13, 19] = 19


class BotCreateSchema(GameCreateSchema):
    bot_rating: int = 1000
    handicap: int = Field(0, ge=0, le=9)
    komi: float = 6.5
    player_color: Literal["black", "white", "random"] = "random"
