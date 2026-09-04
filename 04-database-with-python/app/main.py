import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from psycopg.rows import dict_row
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def get_posts():
    with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
             dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM posts")
        posts = cur.fetchall()
    return {"data": posts}

@app.post("/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
             dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO posts (title, content)
        VALUES (%s, %s) RETURNING * """, (post.title, post.content))
        new_post = cur.fetchone()
        conn.commit()
        return [{"post created": new_post}]

@app.get("/{id}")
def get_post(id: int):
    with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
                 dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
            post = cur.fetchone()
            if not post:
                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                     detail=f"Post with id: {id} isn't present")
            return {"data": post}

@app.delete("/{id}")
def delete_post(id: int):
     with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
                      dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
          cur.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
          deleted_post = cur.fetchone()
          conn.commit()
          if not deleted_post:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                    detail=f"Post with id: {id} isn't present")
          return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/{id}")
def update_post(id: int, post: Post):
     with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
                           dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
          cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *",
                      (post.title, post.content, id))
          updated_post = cur.fetchone()
          conn.commit()
          if not updated_post:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                                   detail=f"Post with id: {id} isn't present")
          return {"updated post": updated_post}