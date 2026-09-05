from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True