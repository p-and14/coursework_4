import base64
import hashlib
import hmac
from typing import Union

from flask import current_app

from ..dao.main import UsersDAO
from ..exceptions import RegisterError, DataError


class UsersService:
    def __init__(self, dao: UsersDAO):
        self.dao = dao

    def get_by_id(self, uid: int):
        return self.dao.get_by_id(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data: dict):
        password = user_data["password"]

        if len(password) < 1:
            raise DataError('Password not specified.')

        generated_password = self.generate_password(password)
        user_data["password"] = generated_password

        if self.get_by_email(user_data["email"]):
            raise RegisterError(f'User with email = {user_data["email"]} is busy.')

        return self.dao.create(user_data)

    def update(self, user):
        return self.dao.update(user)

    def generate_password(self, password: str) -> bytes:
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            current_app.config['PWD_HASH_SALT'],
            current_app.config['PWD_HASH_ITERATIONS'],
        )

        return base64.b64encode(hash_digest)

    def get_by_username(self, username: str):
        return self.dao.get_by_username(username)

    def get_by_email(self, email: str):
        return self.dao.get_by_email(email)

    def compare_passwords(self, password_hash: Union[str, bytes], other_password: str) -> bool:
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode("utf-8"),
            current_app.config['PWD_HASH_SALT'],
            current_app.config['PWD_HASH_ITERATIONS'],
        )

        hash_digest_b64 = base64.b64encode(hash_digest)

        return hmac.compare_digest(password_hash, hash_digest_b64)

    def change_password(self, user, data: dict):
        if len(data["old_password"]) < 1 or len(data["new_password"]) < 1:
            raise DataError('Password not specified.')

        if not self.compare_passwords(user.password, data["old_password"]):
            raise DataError('Wrong password.')

        user.password = self.generate_password(data["new_password"])

        return user
