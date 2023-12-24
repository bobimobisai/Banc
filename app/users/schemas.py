from datetime import datetime
from pydantic import BaseModel, Field


class User_id(BaseModel):
    user_id: int


class Token_data(BaseModel):
    user_id: int


class UserModel(BaseModel):
    user_id: str
    email: str | None = None


class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    date_birt: str
    phone_number: str


class NewUserAuthModel(BaseModel):
    password: str
    email: str
