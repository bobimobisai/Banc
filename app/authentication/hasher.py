from passlib.context import CryptContext
from pathlib import Path

pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__ident="2b")


class Hasher:
    @staticmethod
    def verif_password(get_password: str, load_password: str) -> bool:
        return pwd_context.verify(get_password, load_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
