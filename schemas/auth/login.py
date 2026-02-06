from pydantic import BaseModel, Field


class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
