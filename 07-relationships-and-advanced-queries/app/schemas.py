from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True

class OwnerPostResponse(BaseModel):
    id: int
    email: EmailStr

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    owner_id: int
    owner: OwnerPostResponse

    model_config = ConfigDict(from_attributes = True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)

class VoteDir(IntEnum):
    down = 0
    up = 1

class Vote(BaseModel):
    post_id: int
    dir: VoteDir