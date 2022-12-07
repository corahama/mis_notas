from pydantic import BaseModel, EmailStr
from datetime import datetime


class Note(BaseModel):
    title: str
    content: str

class NoteRes(Note):
    id: int
    owner: int
    created_at: datetime

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str

class UserRes(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
