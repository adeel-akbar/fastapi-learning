from random import randrange

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()
new_posts = [{"title": "title of post 1", "content": "content of post 1",
              "id": 1}, {"title": "post 2", "content": "About section",
                           "id": 2}]
def find_post(id):
    for post in new_posts:
        if post['id'] == id:
            return post

def find_index(id):
    for i, post in enumerate(new_posts):
        if post["id"] == id:
            return i
class Post(BaseModel):
    title: str
    content: str

#  Getting all posts.
@app.get("/posts")
def get_posts():
    return {"data": new_posts}

# Creating a post. With correct status code 201 created after successful 
# creation.
@app.post("/posts", status_code=status.HTTP_201_CREATED)  
def create_post(post: Post):    
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1, 1000)
    new_posts.append(post_dict)
    return {"data": post_dict}

# Getting a single post by id but as we are not dealing with database
# yet so we will use a function for this.

@app.get("/posts/{id}")    # Adding a http exception if the id isn't present
def get_post(id: int):     # rather then showing nothing.
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"The post with id: {id} isn't available")
    return {"data": post}

# Delete a post. But for that first we have to find the index of that post
# using a function.
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} isn't available")
    new_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Updating a post. Using find_index() function. 
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"The post with id: {id} isn't available")
    post_dict = post.model_dump()
    post_dict["id"] = id
    new_posts[index] = post_dict
    return {"data": post_dict}