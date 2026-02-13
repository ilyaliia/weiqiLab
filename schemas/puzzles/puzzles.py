from pydantic import BaseModel
from typing import Optional


class PuzzleSchema(BaseModel):
    sgf: str
    difficulty: str
    category: str
    author: Optional[str] = None
