from authentication.hasher import Hasher
from data_base.DataBase import DataBase
from schemas.schemas import pars

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
        set_user = "INSERT INTO user (first_name, last_name, father_name, date_birt, phone_number) VALUES(%s, %s, %s, %s, %s);"
        db.set_data(insert_query=set_user, value=user_info_values, transaction=True)
        get_user_id_query = "SELECT LAST_INSERT_ID();"
        user_id = db.get_data(from_get=get_user_id_query, transaction=True)[0][0]
        auth_insert_query = (
            "INSERT INTO user_auth (password, gmail, user_id) VALUES (%s, %s, %s);"
        )
        hash_password = Hasher.get_password_hash(data_user_auth["password"])
        auth_values = (
            hash_password,
            data_user_auth["email"],
            user_id,
        )
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


# внесение парспортных данных
def get_aprove_passport(passport_id: int, SSN_num: int, user_id: int):
    try:
        data = (passport_id, SSN_num, user_id)
        set_user_auth = "INSERT INTO user_document (passport_id, SSN_num, user_id) VALUES (%s, %s, %s)"
        db.set_data(insert_query=set_user_auth, value=data)
    except Exception as e:
        return {"Status": "ERROR", "error": e}
    else:
        return {"Status": "SUCCESS"}


# создание счета
def create_bill(user_id: int, type_bill: str, limit: str):
    try:
        data = (user_id, type_bill, 0, limit, "de_active")
        set_user_auth = "INSERT INTO user_bill (user_id, type_bill, ballans, limit_bill, status_bill)VALUES (%s, %s, %s, %s, %s)"
        db.set_data(insert_query=set_user_auth, value=data)
    except Exception as e:
        return {f"eror - {e}"}
    else:
        return True


# сощдание логина и пароля
def auth_userr_data(email: str, passwor: str, user_id: int):
    try:
        data = (passwor, email, user_id)
        set_user_auth = (
            "INSERT INTO user_auth (password, gmail, user_id) VALUES(%s, %s, %s)"
        )
        db.set_data(insert_query=set_user_auth, value=data)
    except Exception as e:
        return {f"eror - {e}"}
    else:
        return True


# создание аккаунта
def create_account(data: tuple):
    if len(data) >= 5 and type(data) is tuple:
        try:
            set_user = "INSERT INTO user (first_name, last_name, father_name, date_birt, phone_number) VALUES(%s, %s, %s, %s, %s);"
            db.set_data(insert_query=set_user, value=data)
        except Exception as e:
            return {f"Eror - {e}"}
        else:
            return {"Data is set SUCCESS!"}
        finally:
            pass
    else:
        return {"len(data) >= 5 and type(data) is tuple"}


# деактивация счета
def deactivate_bill(bill_id):
    try:
        db.open_connection()
        start_tr = "START TRANSACTION;"
        db.get_data(from_get=start_tr, transaction=True)
        query = f"UPDATE user_bill SET status_bill = 'de_active' WHERE bill_idd = {bill_id};"
        db.set_data(insert_query=query, transaction=False)
        return {"Status": "Bill deactivated SUCCESS!"}
    except Exception as e:
        db.connection.rollback()
        return {"Error": e}


# удаление счета пользователя
def del_user_bill(bill_id):
    try:
        qwery = f"SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill WHERE user_bill.bill_idd = {bill_id};"
        zapros = db.get_data(from_get=qwery, transaction=True)
        formt = pars(data_bill=zapros)
        for i in formt["USER_BILL"]:
            if i["ballans"] >= 0 and i["status_bill"] == "de_active":
                qwery_1 = f"DELETE FROM user_bill WHERE bill_idd = {bill_id};"
                db.set_data(insert_query=qwery_1)
                return {"Status": "Deleted SUCCESS!"}
            else:
                return {
                    "ERROR_DELET": [
                        {"CHECK BALANCE(ballans>=0)": i["ballans"]},
                        {"CHECK STATUS BILL(de_active)": i["status_bill"]},
                    ]
                }
    except Exception as e:
        return {"Error": e}
