from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from authentication.Authentic_user import Authentication_user
from jwt import DecodeError
from jwt.exceptions import ExpiredSignatureError
from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional
from users.User import User
from authentication.schemas import Token
from authentication.auth_utils import encode_jwt


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def auth_user(user_data: OAuth2PasswordRequestForm = Depends()):
    user_model = Authentication_user(
        email=user_data.username,
        user_password=user_data.password,
    )
    if user_model["Status"] != "error":
        access_token = encode_jwt(user_model, expire_minute=2)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
