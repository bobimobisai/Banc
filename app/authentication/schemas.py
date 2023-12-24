from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr


class Userr(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None
