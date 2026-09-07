from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas, utilis
from ..database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)
@router.post("/", response_model = schemas.UserResponse ,
          status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utilis.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model = schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                    detail = f"User with id: {user_id} not found..")
    return user