from typing import Annotated
from DataBase import DataBase
from schemas import pars
from decimal import Decimal
from pydantic import BaseModel
from app.authentication.hasher import Hasher

db = DataBase(
    host="127.0.0.1",
    port=3306,
    user="Root_Adm",
    password="Koshkin3322!",
    database="test_name",
)
db.open_connection()


def set_full_user_data(data_user_info: dict, data_user_auth: dict):
    try:
        db.open_connection()
        start_tr = "START TRANSACTION;"
        db.get_data(from_get=start_tr, transaction=True)
        user_info_values = (
            data_user_info["first_name"],
            data_user_info["last_name"],
            data_user_info["father_name"],
            data_user_info["date_birt"],
            data_user_info["phone_number"],
        )
        print(user_info_values)
        set_user = "INSERT INTO user (first_name, last_name, father_name, date_birt, phone_number) VALUES(%s, %s, %s, %s, %s);"
        db.set_data(insert_query=set_user, value=user_info_values, transaction=True)
        get_user_id_query = "SELECT LAST_INSERT_ID();"
        user_id = db.get_data(from_get=get_user_id_query, transaction=True)[0][0]
        auth_insert_query = (
            "INSERT INTO user_auth (password, gmail, user_id) VALUES (%s, %s, %s);"
        )
        hash_password = Hasher.get_password_hash(data_user_auth["password"])
        auth_values = (hash_password, data_user_auth["email"], user_id)
        db.set_data(insert_query=auth_insert_query, value=auth_values, transaction=True)
    except Exception as e:
        return {"Status": "ERROR", "error": e}
    finally:
        qwery = f"SELECT user.phone_number, user_auth.user_id, user_auth.gmail FROM user_auth JOIN user ON user.id = user_auth.user_id WHERE user.id = {user_id};"
        res = db.get_data(from_get=qwery, transaction=True)
        conv = (data_user_info["phone_number"], user_id, data_user_auth["email"])
        if res[0] == conv:
            db.connection.commit()
            db.connection.close()
            return {"Status": "SUCCESS"}
        else:
            db.connection.rollback()
            return {"Status": "ERROR", "error": "when adding data"}


class NewUserModel(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    date_birt: str
    phone_number: str


class NewUserAuthModel(BaseModel):
    password: str
    email: str


def add_new_user(data_user_info: NewUserModel, data_user_auth: NewUserAuthModel):
    res = Annotated[
        dict,
        set_full_user_data(data_user_info, data_user_auth),
    ]
    return res


data_1 = {
    "first_name": "Виктор",
    "last_name": "Прунин",
    "father_name": "Андреевич",
    "date_birt": "1998-05-22",
    "phone_number": "+79558742512",
}
data_2 = {"password": "smetaBuser2432", "email": "McGregor345@gmail.com"}

func = add_new_user(data_1, data_2)
print(func)
