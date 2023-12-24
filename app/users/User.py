from CRUD.CRUD import (
    up_ballans,
    transfer_money,
    put_money,
    create_bill,
    deactivate_bill,
    del_bill,
    change_email,
    change_password,
    change_phone_num,
    user_full_info,
    set_admin_auth_data,
    verif_admin,
)


class User:
    def __init__(self, idd):
        self.idd = idd
        self.data = user_full_info(self.idd)

        self._USER_DATA = False
        self._OPERATION = False
        self._TRANSACTION = False

        self._check_accout_info(self.data)

    def _check_accout_info(self, data):
        if data is not None:
            self._USER_DATA = True
            if data["USER_INFO"]["status_aprove"] == "aprove":
                self._OPERATION = True
                if any(bill["status_bill"] == "active" for bill in data["USER_BILL"]):
                    self._TRANSACTION = True

    def _get_info(self):
        return {
            "USER_PERMISSION": {
                "Status User_document/bill": self._USER_DATA,
                "Status User_verification": self._OPERATION,
                "Status User_bill_active": self._TRANSACTION,
            },
            "USER_DATA": {"Data": self.data},
        }

    def user_up_balance(self, summ_set: float, bill_id: int = 0):
        if self._USER_DATA is True and self._OPERATION is True:
            if any(bill["bill_idd"] == bill_id for bill in self.data["USER_BILL"]):
                res = up_ballans(summ_set=summ_set, bill_up_id=bill_id)
                return res
            else:
                return {"Status": "BILL_UP_ERROR"}
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_transaction(
        self,
        summ_send: float,
        bill_sender_idd: int,
        bill_recip_idd: int,
    ):
        if (
            self._USER_DATA is True
            and self._OPERATION is True
            and self._TRANSACTION is True
        ):
            if any(
                bill["bill_idd"] == bill_sender_idd for bill in self.data["USER_BILL"]
            ):
                try:
                    res = transfer_money(
                        summ_send=summ_send,
                        bill_sender_idd=bill_sender_idd,
                        bill_recip_idd=bill_recip_idd,
                    )
                    return res
                except UnboundLocalError:
                    return {"Status": "ERROR", "error": "check payment"}
            else:
                return {"Status": "BILL_UP_ERROR"}
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_put_money(self, bill_id: int, summ_put: float):
        if (
            self._USER_DATA is True
            and self._OPERATION is True
            and self._TRANSACTION is True
        ):
            if any(bill["bill_idd"] == bill_id for bill in self.data["USER_BILL"]):
                res = put_money(bill_id=bill_id, summ_put=summ_put)
                return res
            else:
                return {"Status": "BILL_UP_ERROR"}
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_create_bill(self, type_bill: str, limit: str = "no_limit"):
        if self._USER_DATA is True and self._OPERATION is True:
            if all(bill["type_bill"] != type_bill for bill in self.data["USER_BILL"]):
                if limit in ["no_limit", "limit_1", "limit_2"] and type_bill in [
                    "debit",
                    "debit_EUR",
                    "credit",
                ]:
                    res = create_bill(
                        user_id=self.idd,
                        type_bill=type_bill,
                        limit=limit,
                        _status_bill="active",
                    )
                    return res
                else:
                    return {"Status": "UNKNOWN_BILL_TYPE_OR_LIMIT"}
            else:
                return {"Status": "TWO_BILL_ERROR"}
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_deactivate_bill(self, bill_id: int):
        if (
            self._USER_DATA is True
            and self._OPERATION is True
            and self._TRANSACTION is True
        ):
            res = deactivate_bill(bill_id)
            return res
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_del_bill(self, bill_id):
        if self._USER_DATA is True and self._OPERATION is True:
            res = del_bill(bill_id)
            return res
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_change_email(
        self,
        user_email: str,
        user_new_email: str,
        user_password: str,
    ):
        if self._USER_DATA is True:
            res = change_email(
                user_id=self.idd,
                user_email=user_email,
                user_new_email=user_new_email,
                user_password=user_password,
            )
            return res
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_change_password(
        self, user_email: str, user_password: str, user_new_password: str
    ):
        if self._USER_DATA is True:
            res = change_password(
                user_id=self.idd,
                user_email=user_email,
                user_password=user_password,
                user_new_password=user_new_password,
            )
            return res
        else:
            return {"Status": "PERMISSION_ERROR"}

    def user_change_phone_num(self, user_phone_num: str, user_new_phone_num: str):
        if self._USER_DATA is True:
            res = change_phone_num(
                user_id=self.idd,
                user_phone_num=user_phone_num,
                user_new_phone_num=user_new_phone_num,
            )
            return res
        else:
            return {"Status": "PERMISSION_ERROR"}
        pass


class Admin:
    def __init__(self) -> None:
        pass

    def admin_operation_up_ballans(self):
        pass

    def correct_user_data(self):
        pass

    def aprove_documet(self):
        pass

    def aprove_bill(self):
        pass

    def get_user_action(self):
        pass

    def get_user_transaction(self):
        pass

    def admin_set_auth_data(self, email: str, password: str):
        res = set_admin_auth_data(email=email, password=password)
        return res

    def admin_verif_log(self, email: str, password: str):
        res = verif_admin(email=email, password=password)
        return res
