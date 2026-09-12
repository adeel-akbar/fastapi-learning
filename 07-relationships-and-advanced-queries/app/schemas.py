from datetime import datetime

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