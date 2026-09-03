import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from psycopg.rows import dict_row

load_dotenv()
app = FastAPI()

with psycopg.connect(host= os.getenv("host"), password = os.getenv("password"), 
             dbname = os.getenv("dbname"), user = os.getenv("user"), row_factory= dict_row) as conn, conn.cursor() as cur:
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
@app.get("/")
def get_posts():
    return {"data": posts}