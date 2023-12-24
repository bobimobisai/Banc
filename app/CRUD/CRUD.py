from data_base.DataBase import DataBase
from schemas.schemas import pars
from decimal import Decimal
from authentication.hasher import Hasher

db = DataBase(
    host="127.0.0.1",
    port=3306,
    user="Root_Adm",
    password="Koshkin3322!",
    database="test_name",
)
db.open_connection()


# вся инфомация о пользователе и счетах
def user_full_info(user_id: int):
    db.open_connection()
    try:
        user_information = """
                SELECT user.first_name, user.phone_number, user_auth.gmail, user_document.status_aprove
                FROM user
                JOIN user_auth ON user_auth.user_id = user.id  
                JOIN user_document ON user_document.user_id = user.id
                WHERE user.id = %s;
                """
        user_bill_information = """
                SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd
                FROM user 
                JOIN user_bill ON user_bill.user_id = user.id 
                WHERE user.id = %s;
                """
        user_data = db.get_data(
            from_get=user_information, value=user_id, transaction=True
        )
        user_dill = db.get_data(
            from_get=user_bill_information, value=user_id, transaction=False
        )
    except Exception as e:
        return {"Status": "ERROR", "Error_DB/itit": e}
    else:
        if (
            user_data == ()
            or user_data == ((0),)
            or user_data == ((),)
            and user_dill == ()
            or user_dill == ((0),)
            or user_dill == ((),)
            or user_data == (0, "")
        ):
            return None
        else:
            return pars(user_data, user_dill)


# пополнение баланса
def up_ballans(summ_set: float, bill_up_id=0):
    summ = float(summ_set)
    if isinstance(summ, float) and summ >= 10.00:
        db.open_connection()
        start_transaction = "START TRANSACTION;"
        db.get_data(from_get=start_transaction, transaction=True)
        qwer = "SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill WHERE user_bill.bill_idd = %s FOR UPDATE;"
        get_user_bill_data = db.get_data(
            from_get=qwer, value=bill_up_id, transaction=True
        )
        search_bill = pars(data_bill=get_user_bill_data)
        for i in search_bill["USER_BILL"]:
            if i["bill_idd"] == bill_up_id:
                try:
                    sum_update = round(float(i["ballans"]) + summ, 2)
                    id_bill = i["bill_idd"]
                    set_user_ballans = f"UPDATE user_bill SET ballans = {sum_update} WHERE bill_idd = {id_bill}"
                    db.set_data(
                        insert_query=set_user_ballans,
                        types_data="none",
                        transaction=False,
                    )
                except Exception as e:
                    return {"Status": "ERROR", "operation has been cancel": e}
                finally:
                    db.open_connection()
                    qwer_1 = f"SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill JOIN user ON user.id = user_bill.user_id WHERE user_bill.bill_idd = {bill_up_id};"
                    check_data = db.get_data(from_get=qwer_1, transaction=False)
                    search_bill = pars(data_bill=check_data)
                    for i in search_bill["USER_BILL"]:
                        if i["bill_idd"] == bill_up_id:
                            if sum_update == float(i["ballans"]):
                                return {"Status": "SUCCESS", "Ballance": sum_update}
                            else:
                                return {
                                    "Status": "ERROR",
                                    "eror in transaction, check status your bill": sum_update,
                                }
                    return check_data
            else:
                return {"Status": "ERROR", "error": "id_error"}
        else:
            db.close_connection()
            raise Exception(f"none bill - {bill_up_id}")
    else:
        return {"Status": "ERROR", "error": "summ_set <= 10.00!"}


# перевод денег по внутренним счетам
def transfer_money(
    summ_send: float,
    bill_sender_idd: int,
    bill_recip_idd: int,
):
    summ = float(summ_send)
    if isinstance(summ, float) and summ >= 10.00:
        try:
            db.open_connection()
            start_transaktion = "START TRANSACTION;"
            db.get_data(start_transaktion, transaction=True)
            qwer_get = f"SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill WHERE user_bill.bill_idd IN ({bill_sender_idd}, {bill_recip_idd}) FOR UPDATE;"
            get_user_bill_data = db.get_data(qwer_get, transaction=True)
            res_search_bill = pars(data_bill=get_user_bill_data)
            if len(res_search_bill["USER_BILL"]) >= 2:
                for i in res_search_bill["USER_BILL"]:
                    if (
                        i["bill_idd"] == bill_sender_idd
                        and float(i["ballans"]) >= summ
                        and i["status_bill"] == "active"
                    ):
                        send = i
                    if bill_recip_idd == i["bill_idd"] and i["status_bill"] == "active":
                        recip = i
                balans_new_send = round(float(send["ballans"]) - summ, 2)
                balans_new_recip = round(float(recip["ballans"]) + summ, 2)
                qwer = f"UPDATE user_bill SET ballans = CASE WHEN bill_idd = {send['bill_idd']} AND status_bill = 'active' THEN {balans_new_send} WHEN bill_idd = {recip['bill_idd']} AND status_bill = 'active' THEN {balans_new_recip} ELSE ballans END WHERE (bill_idd = {send['bill_idd']} AND status_bill = 'active') OR (bill_idd = {recip['bill_idd']} AND status_bill = 'active');"
                db.set_data(insert_query=qwer, types_data="no")
                db.open_connection()
                g_d = db.get_data(qwer_get, transaction=False)
                res_search_bill = pars(data_bill=g_d)
                ASEPT = []
                for i in res_search_bill["USER_BILL"]:
                    if float(i["ballans"]) == balans_new_send:
                        ASEPT.append("ASEPT")
                    if float(i["ballans"]) == balans_new_recip:
                        ASEPT.append("ASEPT")
                if ASEPT[0] == "ASEPT" and ASEPT[1] == "ASEPT":
                    return {"Status": "SUCCESS", "Ballans_sender": balans_new_send}
                else:
                    raise Exception({"ERROR": "BALANCE SENDER DO NOT UPDATE"})
            else:
                return {"Status": "ERROR", "error": "Bill not found"}
        except Exception as e:
            raise e
    else:
        return {"Status": "ERROR", "Summ send >= 10.00": summ_send}


# заполение данных о пользователе (фио, дата рождения, номер телефона) + (логин, пароль)
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
        auth_values = (
            data_user_auth["password"],
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
def create_bill(user_id: int, type_bill: str, limit: str, _status_bill="de_active"):
    try:
        data = (user_id, type_bill, 0, limit, _status_bill)
        set_user_auth = "INSERT INTO user_bill (user_id, type_bill, ballans, limit_bill, status_bill)VALUES (%s, %s, %s, %s, %s)"
        db.set_data(insert_query=set_user_auth, value=data)
    except Exception as e:
        return {"Status": "ERROR", "error": e}
    else:
        return {"Status": "SUCCESS"}


# сощдание логина и пароля
def auth_userr_data(email: str, passwor: str, user_id: int):
    try:
        data = (passwor, email, user_id)
        set_user_auth = (
            "INSERT INTO user_auth (password, gmail, user_id) VALUES(%s, %s, %s)"
        )
        db.set_data(insert_query=set_user_auth, value=data)
    except Exception as e:
        return {"Status": "ERROR", "error": e}
    else:
        return {"Status": "SUCCESS"}


# создание аккаунта
def create_account(data: tuple):
    if len(data) >= 5 and type(data) is tuple:
        try:
            set_user = "INSERT INTO user (first_name, last_name, father_name, date_birt, phone_number) VALUES(%s, %s, %s, %s, %s);"
            db.set_data(insert_query=set_user, value=data)
        except Exception as e:
            return {"Status": "ERROR", "error": e}
        else:
            return {"Status": "SUCCESS"}
        finally:
            pass
    else:
        return {"Status": "ERROR", "error": "len(data) >= 5 and type(data) is tuple"}


# деактивация счета
def deactivate_bill(bill_id):
    try:
        db.open_connection()
        start_tr = "START TRANSACTION;"
        db.get_data(from_get=start_tr, transaction=True)
        query = f"UPDATE user_bill SET status_bill = 'de_active' WHERE bill_idd = {bill_id};"
        db.set_data(insert_query=query, transaction=False)
        return {"Status": "SUCCESS"}
    except Exception as e:
        db.connection.rollback()
        return {"Error": e}


# удаление счета юзера
def del_bill(bill_id):
    try:
        qwery = f"SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill WHERE user_bill.bill_idd = {bill_id};"
        zapros = db.get_data(from_get=qwery, transaction=True)
        formt = pars(data_bill=zapros)
        for i in formt["USER_BILL"]:
            if i["ballans"] == 0 and i["status_bill"] == "de_active":
                qwery_1 = f"DELETE FROM user_bill WHERE bill_idd = {bill_id};"
                db.set_data(insert_query=qwery_1)
                return {"Status": "SUCCESS"}
            else:
                return {
                    "Status": "ERROR",
                    "ERROR_DELET": [
                        {"CHECK BALANCE(ballans>=0)": i["ballans"]},
                        {"CHECK STATUS BILL(de_active)": i["status_bill"]},
                    ],
                }
    except Exception as e:
        return {"Status": "ERROR", "Error": e}


# снятие денег
def put_money(bill_id: int, summ_put: float):
    sum_put = float(summ_put)
    if sum_put >= 10:
        try:
            qwery = f"SELECT user_bill.type_bill, user_bill.ballans, user_bill.limit_bill, user_bill.status_bill, user_bill.bill_idd FROM user_bill WHERE user_bill.bill_idd = {bill_id};"
            zapros = db.get_data(from_get=qwery, transaction=True)
            formt = pars(data_bill=zapros)
            for i in formt["USER_BILL"]:
                if (
                    i["ballans"] >= sum_put
                    and i["status_bill"] == "active"
                    and i["limit_bill"] == "no_limit"
                ):
                    new_ballans = round(i["ballans"] - sum_put, 2)
                    qwery_2 = f"UPDATE user_bill SET user_bill.ballans = {new_ballans} WHERE user_bill.bill_idd = {bill_id};"
                    db.set_data(insert_query=qwery_2)
                    return {"Status": "SUCCESS", "New_ballans": new_ballans}
                else:
                    return {
                        "Status": "ERROR",
                        "ERROR": "summ_put < ballans or limit_bill or status_bill",
                    }
        except Exception as e:
            return {"Status": "ERROR", "error": e}
    else:
        return {"Status": "ERROR", "ERROR": "summ < 10"}


def change_email(
    user_id: int,
    user_email: str,
    user_new_email: str,
    user_password: str,
):
    qwery = (
        "SELECT user_auth.gmail, user_auth.password FROM user_auth WHERE user_id = %s"
    )
    try:
        get_user_data = db.get_data(from_get=qwery, value=user_id, transaction=True)
        user_verif_password = Hasher.verif_password(user_password, get_user_data[0][1])
        if user_email == get_user_data[0][0] and user_verif_password is True:
            qwery = "UPDATE user_auth SET gmail = %s WHERE user_id = %s;"
            db.set_data(insert_query=qwery, value=(user_new_email, user_id))
            return {"Status": "SUCCESS", "New_email": user_new_email}
        else:
            db.close_connection()
            return {"Status": "ERROR", "ERROR": "old email or password dont match!"}
    except Exception as e:
        return {"Status": "ERROR", "ERROR": e}


def change_password(
    user_id: int,
    user_email: str,
    user_password: str,
    user_new_password: str,
):
    qwery = (
        "SELECT user_auth.gmail, user_auth.password FROM user_auth WHERE user_id = %s"
    )
    try:
        get_user_data = db.get_data(from_get=qwery, value=user_id, transaction=True)
        user_verif_password = Hasher.verif_password(user_password, get_user_data[0][1])
        if user_email == get_user_data[0][0] and user_verif_password is True:
            qwery_1 = "UPDATE user_auth SET password = %s WHERE user_id = %s;"
            new_pass = Hasher.get_password_hash(user_new_password)
            db.set_data(insert_query=qwery_1, value=(new_pass, user_id))
            return {"Status": "SUCCESS"}
        else:
            db.close_connection()
            return {"Status": "ERROR", "ERROR": "old email or password dont match!"}
    except Exception as e:
        return {"Status": "ERROR", "ERROR": e}


def change_phone_num(user_id: int, user_phone_num: str, user_new_phone_num: str):
    try:
        qwery = "SELECT user.phone_number FROM user WHERE user.id = %s"
        get_user_num = db.get_data(qwery, value=user_id, transaction=True)
        if user_phone_num == get_user_num[0][0]:
            qwery_1 = "UPDATE user SET phone_number = %s WHERE user.id = %s;"
            db.set_data(qwery_1, value=(user_new_phone_num, user_id))
            return {"Status": "SUCCESS"}
        else:
            db.close_connection()
            return {"Status": "ERROR", "ERROR": "phone number dont match!"}
    except Exception as e:
        return {"Status": "ERROR", "ERROR": e}


def set_admin_auth_data(email, password):
    try:
        hash_pass = Hasher.get_password_hash(password)
        data = (email, hash_pass)
        qwery = "INSERT INTO admin_auth (admin_email, hash_password) VALUE(%s, %s)"
        db.set_data(qwery, value=data)
    except Exception as e:
        print(e)


def verif_admin(email: str, password: str):
    try:
        qwery = (
            "SELECT admin_email, hash_password FROM admin_auth WHERE admin_email = %s"
        )
        get_email = db.get_data(from_get=qwery, value=email)
        hash_pass = Hasher.verif_password(password, get_email[0][1])
        if get_email[0][0] == email and hash_pass is True:
            return True
        else:
            return {"Status": "ERROR"}
    except Exception as e:
        return {"Status": "ERROR", "error": e}

