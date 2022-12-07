from datetime import datetime, timedelta

from jose import jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import database, models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="logn")

SECRET_KEY = "d015554f20cb1094c0e0b151f8882dfaa32217dc333451e4e937f87bb5bc5428"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 10


def create_access_token(payload: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str,credentials_exception):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("user_id")

    if user_id is None:
        raise credentials_exception

    return user_id

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales", headers={"WWW-Authenticate": "Bearer"})

    user_id = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No existe ningún \
usuario asociado al id proporcionado")

    return user
