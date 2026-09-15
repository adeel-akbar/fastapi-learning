from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..config import settings
from ..database import get_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl = "login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
token_expire_time = settings.TOKEN_EXPIRE_TIME

def create_token(data: dict):
    copy_of_data = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = token_expire_time)
    copy_of_data.update({"exp": expire})
    access_token = jwt.encode(copy_of_data, SECRET_KEY, algorithm = ALGORITHM)
    return access_token

def get_current_user(token: str = Depends(oauth_scheme), 
            db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Credentials",
        headers = {"WWW-AUTHENTICATE": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user = db.execute(select(models.User).where(models.User.id == user_id)).scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user