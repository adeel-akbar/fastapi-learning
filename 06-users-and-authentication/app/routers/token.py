import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
token_expire_time = 30

def create_token(data: dict):
    expire = datetime.now() + timedelta(minutes = token_expire_time)
    data.update({"exp": expire})
    access_token = jwt.encode(data, SECRET_KEY, algorithm = ALGORITHM)
    return access_token

def get_current_user(token: str = Depends(oauth_scheme), 
            db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials",
        headers = {"WWW-AUTHENTICATE": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = ALGORITHM)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user