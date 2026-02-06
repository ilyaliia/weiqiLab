from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    email: str
    password: str

