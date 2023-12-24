from typing import Annotated
from fastapi import Depends, HTTPException, status

from passlib.context import CryptContext
from pathlib import Path
from users.User import User
import jwt
from jwt import DecodeError
from jwt.exceptions import ExpiredSignatureError

from pydantic import BaseModel
from datetime import timedelta, datetime





class AuthJWT(BaseModel):
    privat_key_path: Path = Path(
        "C:/Users/Cyber/PycharmProjects/VS_Data_base_learn/certs/jwt-privat.pem"
    )
    public_key: Path = Path(
        "C:/Users/Cyber/PycharmProjects/VS_Data_base_learn/certs/jwt-public.pem"
    )
    algorithm: str = "RS256"
    access_token_expire_minute: int = 3


def encode_jwt(
    payload: dict,
    key=AuthJWT().privat_key_path.read_bytes(),
    algorithm=AuthJWT().algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minute: int = 15,
):
    encode_up = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minute)
    encode_up.update(exp=expire, iat=now)
    encoded = jwt.encode(encode_up, key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token, public_key=AuthJWT().public_key.read_bytes(), algorithm=AuthJWT().algorithm
):
    try:
        decoded = jwt.decode(token, public_key, algorithms=algorithm)
        return decoded
    except DecodeError as e:
        return {"ERROR": e}
    except ExpiredSignatureError as e:
        return {"ERROR": e}


# check token
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        else:
            return user_id
    except Exception:
        raise credentials_exception
