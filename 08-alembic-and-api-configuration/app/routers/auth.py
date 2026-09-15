from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..utilis import verify
from .token import create_token

router = APIRouter()

@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(select(models.User).where(models.User.email == user_credentials.username)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Invalid Credentials")
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                    detail = "Invalid Credentials")
    token = create_token({"user_id": user.id})
    return {"token": token, "token_type": "bearer"}


    