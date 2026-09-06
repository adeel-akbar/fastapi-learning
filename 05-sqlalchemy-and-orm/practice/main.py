from fastapi import FastAPI

from . import models
from .database import engine

app = FastAPI()
models.Base.metadata.create_all(bind= engine)

@app.get("/")
def get_posts():
    return {"message": "done"}