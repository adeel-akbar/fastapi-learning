from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind = engine)
app = FastAPI()

@app.get("/")
def get_posts(db: Session = Depends(get_db)):
    return {"message": "done"}