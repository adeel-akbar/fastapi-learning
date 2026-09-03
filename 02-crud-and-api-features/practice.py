from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

app = FastAPI()
# Practice 1 — Find by ID

# Create a function:
# def find_post(id):
# that searches this:
# posts = [
#     {"id": 1, "title": "Python"},
#     {"id": 2, "title": "FastAPI"},
#     {"id": 3, "title": "PostgreSQL"}
# ]
# Return the matching post.
# Test:
# find_post(2)
# Expected:
# {"id": 2, "title": "FastAPI"}
# And test an ID that doesn't exist.

posts = [
    {"id": 1, "title": "Python"},
    {"id": 2, "title": "FastAPI"},
    {"id": 3, "title": "PostgreSQL"}
]
def find_post(id):
    for post in posts:
        if post["id"] == id:
            return post
        
@app.get("/posts/{id}")
def post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"The post with id: {id} isn't available")
    return {"data": post}
# If the id of the post is present it will simply show that post if not present
# it will show an 404 error with message that post isn'r available.

# Practice 2 — Create a Post

# Create:
# POST /practice/posts
# Use a Pydantic model:
# class Post(BaseModel):
#     title: str
#     content: str
# When a request comes in, add a new post to a list.
# Return the newly created post.
# Don't look at your Chapter 2 code while doing this.

my_posts = [
    {"title": "Python", "content": "Python is a programming language"},
    {"title": "FastAPI", "content": "FastAPI is a framework"}
]

class Post(BaseModel):
    title: str
    content: str

@app.get("/practice/post")
def get_posts():
    return {"posts":my_posts}

@app.post("/practice/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    my_posts.append(post_dict)
    return {"new post": post_dict}

# Here i also added get posts to check if the posts had been added successfully.

# Practice 3 — Delete by ID ⭐

# Create:
# DELETE /practice/posts/{id}
# Requirements:
# Find the post.
# Delete it if it exists.
# If it doesn't exist → return 404.
# If successful → return 204.
# This is especially good practice because you need to think about index vs ID.

new_posts = [
    {"id": 1, "title": "Python", "content": "Python is a programming language"},
    {"id": 2, "title": "FastAPI", "content": "FastAPI is a framework"}
]

def find_index(id):
    for i, post in enumerate(new_posts):
        if post['id'] == id:
            return i

@app.delete("/practice/post/{id}")
def delete_post(id: int):
    index = find_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The post with id: {id} isn't available")
    new_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Practice 4 — Update by ID ⭐⭐

# Create:
# PUT /practice/posts/{id}
# Request:
# {
#     "title": "Updated title",
#     "content": "Updated content"
# }
# Requirements:
# Find the post.
# If it doesn't exist → 404.
# Replace its title/content.
# Keep the same ID.
# Return the updated post.

@app.put("/practice/post/{id}")
def update_post(id: int, post: Post):
    index = find_index(id)
    if index is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail= f"The post with id: {id} isn't available")
    post_dict = post.model_dump()
    post_dict['id'] = id
    new_posts[index] = post_dict
    return {"updated post": post_dict}


# Practice 5 — API behavior challenge

# Suppose your API currently contains:
# posts = [
#     {"id": 1, "title": "Python"},
#     {"id": 2, "title": "FastAPI"},
#     {"id": 3, "title": "PostgreSQL"}
# ]
# Without running the code, tell me what should happen for each:
# A.
# GET /posts
'''Return all the posts 200 ok'''
# B.
# GET /posts/2
'''Return's the post with id: 2: {"id": 2, "title": "FastAPI"} 200 ok '''
# C.
# GET /posts/99
'''Return error 404 not found'''
# D.
# DELETE /posts/2
'''Delete the second post {"id": 2, "title": "FastAPI"} returns 204 no content'''
# E.
# DELETE /posts/99
'''Returns error 404 not found'''
# F.
# PUT /posts/1
# with:
# {
#     "title": "Advanced Python",
#     "content": "Learning backend development"
# }
'''Update the post 1 with status 200 ok '''
# For each, tell me the status code + result.