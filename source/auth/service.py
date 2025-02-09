from sqlalchemy.exc import IntegrityError

from source.auth.models import User
from source.auth.schemas import SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery
from source.auth.utils import hash_password, verify_password
from source.database_service.Base import BaseService
from source.exceptions.auth_exc import exceptions


class UsersService(BaseService[User, SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery]):

    model = User
    filter_model_scheme = SUserFilterQuery
    update_model_scheme = SUserUpdateQuery
    model_node_scheme = SUserInsertQuery

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> User:
        user = await cls.get_one_or_none(email=email)
        if not user:
            raise exceptions.UserIsNotExistException("User is not exist")

        password_is_valid = verify_password(password, str(user.hashed_password))
        if not password_is_valid:
            raise exceptions.PasswordIsInvalidException("Password is not valid")

        return user

    @classmethod
    async def set_refresh_token_id(cls, token_id: str, user_id: int):
        if not await cls.get_by_id(user_id):
            raise exceptions.UserIsNotExistException("User is not exist")

        filter_by = {"id": user_id}
        values = {"refresh_token_id": token_id}
        try:
            await cls.update_node(filter_by, values)
        except IntegrityError:
            raise exceptions.RefreshTokenSetException("Failed to set a refresh token in the DB")

    @classmethod
    async def switch_password(cls, old_password: str, new_password: str, user_email: str):
        await cls.authenticate_user(user_email, old_password)

        hashed_password = hash_password(new_password)

        filter_by = {"email": user_email}
        values = {"hashed_password": hashed_password}
        try:
            await cls.update_node(filter_by, values)
        except IntegrityError:
            raise exceptions.PasswordChangeException(("Failed to change a password in the DB"))
