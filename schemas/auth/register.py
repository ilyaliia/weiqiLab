from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    password_confirm: str
