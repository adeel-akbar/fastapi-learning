import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
# Chapter 4 — Practice Set

# 1. Connect Python to PostgreSQL
# Write Python code using psycopg to connect to your fastapi database 
# using credentials from .env.
conn = psycopg.connect(host= os.getenv("host"), dbname= os.getenv("dbname"),
row_factory=dict_row, user= os.getenv("user"), password= os.getenv("password"))
cur = conn.cursor()
# 2. Read all posts

# Write code that:
# connects to PostgreSQL
# executes SELECT * FROM posts
# fetches all posts
# prints them

@app.get("/")
def get_posts():
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    return {"data": posts}

# 3. Find a post by ID

# Write a function:
# get_post(id)
# that retrieves a post from the posts table using its ID.
# If the post doesn't exist, print:
# Post not found

@app.get("/{id}")
def get_post(id: int):
    cur.execute("""SELECT * FROM posts
    WHERE id= %s""", (id,))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found")
    return {"data": post}

# 4. Create a post

# Write code that inserts a new post into the database:
# title = "My first database post"
# content = "Learning PostgreSQL with Python"
# Use a parameterized query rather than putting the values directly 
# into the SQL string.

class Post(BaseModel):
    title: str
    content: str

@app.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cur.execute('''INSERT INTO posts (title, content)
    VALUES (%s, %s) RETURNING *''', (post.title, post.content))
    new_post= cur.fetchone()
    conn.commit()
    return {"new post": new_post}

# 5. Update a post

# Write code to update the title and content of a post with a particular ID.
# For example:
# id = 1
# title = "Updated title"
# content = "Updated content"
# Use RETURNING * and print the updated post.

@app.put("/{id}")
def update_post(id: int, post: Post):
    cur.execute('''UPDATE posts
    SET title= %s, content= %s
    WHERE id= %s 
    RETURNING *''', (post.title, post.content, id))
    updated_post = cur.fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found")
    return {"updated post": updated_post}

# 6. Delete a post

# Write code to delete a post by ID using:
# DELETE ... RETURNING *
# Print the deleted post.
# If nothing was deleted, print:
# Post not found

@app.delete("/{id}")
def delete_post(id: int):
    cur.execute('''DELETE FROM posts
    WHERE id = %s RETURNING *''', (id,))
    deleted_post = cur.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found")
    print(deleted_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)