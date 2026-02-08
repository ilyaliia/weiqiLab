from pydantic import BaseModel


class MoveSchema(BaseModel):
    coord: str
