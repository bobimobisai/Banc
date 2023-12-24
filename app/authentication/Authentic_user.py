from data_base.DataBase import DataBase
from authentication.hasher import Hasher


class Authentication_user:
    def __new__(cls, email: str, user_password: str):
        db = DataBase(
            host="127.0.0.1",
            port=3306,
            user="Root_Adm",
            password="Koshkin3322!",
            database="test_name",
        )
        db.open_connection()
        ap_info = cls.aprovied_email(email, db)
        if ap_info:
            extract = cls.unpack_tuple(ap_info)
            data_auth = cls.get_auth_data(extract, db)
            if data_auth:
                extract_auth_data = cls.unpack_tuple(data_auth)
                if (
                    email == extract
                    and Hasher.verif_password(user_password, extract_auth_data[0])
                    is True
                ):
                    return {"Status": "Acept", "user_id": extract_auth_data[1]}
                else:
                    return {
                        "Status": "error",
                        "error": "login or password is incorrect",
                    }
            else:
                return {
                    "Status": "error",
                    "error": "FATALL ERROR - DATA IN THE DATABASE IS VIOLATED ",
                }
        else:
            return (
                {
                    "Status": "error",
                    "error": "There is no account for the email you provided",
                },
            )

    @staticmethod
    # функция возвращает id по номеру телефона
    def aprovied_email(email, conect):
        query = "SELECT user_auth.gmail FROM user_auth WHERE gmail=%s"
        result = conect.get_data(from_get=query, value=email, transaction=True)
        return result

    @staticmethod
    # функция возвращает почту и пароль по id
    def get_auth_data(email, conect):
        query = (
            "SELECT user_auth.password, user_auth.user_id FROM user_auth WHERE gmail=%s"
        )
        result = conect.get_data(from_get=query, value=email, transaction=False)
        return result

    @classmethod
    # функция распаковки данных из БД
    def unpack_tuple(self, data):
        if isinstance(data, tuple) and len(data) == 1:
            return self.unpack_tuple(data[0])
        else:
            return data
