from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .token import get_current_user

router = APIRouter(
    prefix = "/posts", 
    tags = ["posts"]
)

@router.get("/", response_model = list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = db.execute(select(models.Post))
    posts = result.scalars().all()
    return posts

@router.post("/", response_model = schemas.PostResponse, status_code = status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_post = models.Post(**post.model_dump(), owner_id = current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model = schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    post = db.execute(select(models.Post).where(models.Post.id == post_id)).scalar_one_or_none()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                    detail = f"Post with id: {post_id} not present..")
    return post

@router.delete("/{post_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    post = result.scalars().one_or_none()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {post_id} not present..")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    db.delete(post)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{post_id}", response_model = schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = db.execute(select(models.Post).where(models.Post.id == post_id))
    the_post = result.scalars().one_or_none()
    if not the_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                                    detail = f"Post with id: {post_id} not present..")
    if the_post.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    for key, value in post.model_dump().items():
        setattr(the_post, key, value)
    db.commit()
    db.refresh(the_post)
    return the_post
