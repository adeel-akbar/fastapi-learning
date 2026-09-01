from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # It will set True by default if we didn't assign anything
    rating: Optional[int] = None  # Its optional and set None by default
    # rating: int | None = None  We can use it this way without bothering with
    # the typing library and importing optional.

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Hello World !!"}

# Using Postman to test our API since we don't have a frontend yet.

@app.post("/create")
def create_posts(data: dict = Body(...)):
    print(data)
    return {"message": "Successfully created a post"}

# Using Schema validation for our post request: 
@app.post("/new_post")
def create_post(post: Post):
    print(post)     # This will print the post in pydantic model style
    print(post.dict())   #This will print post in dict. dict() is a method of pydantic model
    return {"new_post": post}