from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas, utilis
from .database import engine, get_db

app = FastAPI()
models.Base.metadata.create_all(bind= engine)

@app.get("/", response_model = list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

@app.post("/", response_model = schemas.PostResponse, status_code = status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/{post_id}", response_model = schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.execute(select(models.Post).where(models.Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                    detail = f"Post with id: {post_id} not present..")
    return post

@app.delete("/{post_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().one_or_none()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {post_id} not present..")
    db.delete(post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/{post_id}", response_model = schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    the_post = result.scalars().one_or_none()
    if not the_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail = f"Post with id: {post_id} not present..")
    for key, value in post.model_dump().items():
        setattr(the_post, key, value)
    db.commit()
    db.refresh(the_post)
    return the_post

@app.post("/users", response_model = schemas.UserResponse ,
          status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilis.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user