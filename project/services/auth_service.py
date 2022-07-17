import calendar
import datetime
from typing import Callable, Union

import jwt
from flask_restx import abort
from flask import current_app, request

from .users_service import UsersService
from ..exceptions import ItemNotFound, DataError


class AuthService:
    def __init__(self, user_service: UsersService):
        self.user_service = user_service

    def generate_tokens(self, email: str, password: Union[str, bytes, None], is_refresh: bool = False) -> dict:
        user = self.user_service.get_by_email(email)

        if user is None:
            raise ItemNotFound(f'User not found.')

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            "email": user.email,
        }

        min_add = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config["TOKEN_EXPIRE_MINUTES"])
        data["exp"] = calendar.timegm(min_add.timetuple())
        access_token = jwt.encode(
            data,
            current_app.config["JWT_SECRET"],
            algorithm=current_app.config["JWT_ALGORITHM"]
        )

        days_add = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config["TOKEN_EXPIRE_DAYS"])
        data["exp"] = calendar.timegm(days_add.timetuple())
        refresh_token = jwt.encode(
            data,
            current_app.config["JWT_SECRET"],
            algorithm=current_app.config["JWT_ALGORITHM"]
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def approve_tokens(self, refresh_token: str) -> dict:
        try:
            data = jwt.decode(
                jwt=refresh_token,
                key=current_app.config["JWT_SECRET"],
                algorithms=[current_app.config["JWT_ALGORITHM"]]
            )
        except jwt.exceptions.DecodeError:
            raise DataError("Wrong refresh token")

        email = data.get("email")

        return self.generate_tokens(email, None, is_refresh=True)

    def get_email_from_token(self, token: str) -> str:
        try:
            data = jwt.decode(
                jwt=token,
                key=current_app.config["JWT_SECRET"],
                algorithms=[current_app.config["JWT_ALGORITHM"]]
            )
        except jwt.exceptions.DecodeError:
            raise DataError("Wrong access token")

        email = data.get("email")

        return email

    @staticmethod
    def auth_required(func: Callable):
        def wrapper(*args, **kwargs):
            if "Authorization" not in request.headers:
                abort(401)

            data = request.headers["Authorization"]
            token = data.split("Bearer ")[-1]

            if not token:
                abort(403)

            try:
                jwt.decode(
                    jwt=token,
                    key=current_app.config["JWT_SECRET"],
                    algorithms=[current_app.config["JWT_ALGORITHM"]]
                )

            except Exception as e:
                abort(401, f'JWT decode error {e}')

            return func(*args, **kwargs)

        return wrapper
