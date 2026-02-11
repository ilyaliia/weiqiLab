from typing import Optional

from pydantic import BaseModel


class UserUpdateSchema(BaseModel):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    country: Optional[str] = None
    language: Optional[str] = None
