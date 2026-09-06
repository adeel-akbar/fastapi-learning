from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    title: str
    author: str
    published: bool

class BookResponse(BookCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes = True)    