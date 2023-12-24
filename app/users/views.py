from typing import Annotated
from fastapi import APIRouter, Depends
from users.User import User
from authentication.auth_utils import get_current_user
from users.schemas import Token_data, UserModel, NewUserModel, NewUserAuthModel
from fastapi.security import OAuth2PasswordBearer
from users.crud import set_full_user_data, get_aprove_passport

router = APIRouter(prefix="/user", tags=["user"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login/")


@router.post("/new_user/")
def add_new_user(data_user_info: NewUserModel, data_user_auth: NewUserAuthModel):
    res = set_full_user_data(dict(data_user_info), dict(data_user_auth))
    return res


@router.post("/new_user/set_document")
def add_user_document(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    res = get_aprove_passport(passport_id, SSN_num)
    pass


@router.get("/account/")
def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user_id = get_current_user(token)
    user = User(idd=user_id)
    user_account_info = user._get_info()
    return {"User_permission": user_account_info}


@router.post("/account/up_balance/")
def up_user_ballanse(
    summ_set: float, bill_id: int, token: Annotated[str, Depends(oauth2_scheme)]
):
    user_id = get_current_user(token)
    user = User(idd=user_id)
    user_account_info = user.user_up_balance(summ_set, bill_id)
    return {user_account_info}


@router.post("/account/transaction/")
def transaction_user_money(
    summ_send: float,
    bill_sender_idd: int,
    bill_recip_idd: int,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    user_id = get_current_user(token)
    user = User(idd=user_id)
    user_account_info = user.user_transaction(
        summ_send, bill_sender_idd, bill_recip_idd
    )
    return {"transaction": user_account_info}
