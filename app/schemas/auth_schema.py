from pydantic import BaseModel, EmailStr
from datetime import datetime


class BearerSchema(BaseModel):
    bearer: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

