import pytest
from fastapi import HTTPException
from jose import jwt
from pydantic import ValidationError

from source.auth.auth import create_refresh_token, create_session_token
from source.auth.email_service import create_message_for_register, create_unique_url
from source.auth.service import UsersService
from source.auth.utils import hash_password, verify_password
from source.settings import settings


class TestsService:

    @staticmethod
    @pytest.mark.parametrize(
        "username,email,password,result",
        [
            ("user1", "test@email.com", "password", True),
            ("user1", "test2@email.com", "password", False),
            ("user2", "test@email.com", "password", False),
        ],
    )
    async def test_create_user(username, email, password, result):
        query_reslut = await UsersService.insert_into_table(
            username=username, email=email, hashed_password=password
        )
        assert query_reslut == result

    @staticmethod
    @pytest.mark.parametrize(
        "filter_by,validation_error",
        (
            ({"id": 1}, False),
            ({"username": "logintest", "id": 1}, False),
            ({}, True),
            ({"id": "1"}, True),
            ({"error_column": "error"}, True),
        ),
    )
    async def test_get_one_or_none(filter_by: dict, validation_error: bool):
        try:
            assert await UsersService.get_one_or_none(**filter_by)
        except ValidationError:
            assert validation_error

    @staticmethod
    @pytest.mark.parametrize(
        "filter_by,values,validation_error",
        (
            ({"id": 1}, {"refresh_token_id": "123456"}, False),
            ({}, {"refresh_token_id": "123456"}, True),
            ({"id": 1}, {}, True),
            ({"id": "1"}, {"refresh_token_id": "123456"}, True),
            ({"id": 1}, {"refresh_token_id": 123456}, True),
        ),
    )
    async def test_update_node(filter_by: dict, values: dict, validation_error: bool):
        try:
            result = await UsersService.update_node(filter_by=filter_by, values=values)
            assert result
        except ValidationError:
            assert validation_error

    @staticmethod
    @pytest.mark.parametrize(
        "token_id,user_id,http_error",
        (
            ("2523452", 1, False),
            ("2523452", 235245, True),
        ),
    )
    async def test_set_refresh_token_id(token_id: str, user_id: int, http_error: bool):
        try:
            result = await UsersService.set_refresh_token_id(token_id=token_id, user_id=user_id)
            assert result
        except HTTPException:
            assert http_error

    @staticmethod
    @pytest.mark.parametrize(
        "email,password,http_error",
        (
            ("logintest@gmail.com", "password", False),
            ("logintest1234@gmail.com", "password", True),
            ("logintest@gmail.com", "1234qwer", True),
        ),
    )
    async def test_authenticate_user(email: str, password: str, http_error: bool):
        try:
            assert await UsersService.authenticate_user(email=email, password=password)
        except HTTPException:
            assert http_error


class TestsUtils:

    @staticmethod
    @pytest.mark.parametrize("password", ("pass", "1423", "22_@dsh"))
    async def test_hash_password(password: str):
        hashed_password = hash_password(password)
        assert password != hashed_password

    @staticmethod
    @pytest.mark.parametrize("password", ("pass", "1423", "22_@dsh"))
    async def test_verify_password(password: str):
        hashed_password = hash_password(password)
        assert verify_password(password, hashed_password)


class TestsAuth:

    @staticmethod
    async def test_create_session_token():
        user_id = "1"
        session_token = await create_session_token(user_id)

        user_id_from_token = jwt.decode(session_token, settings.SECRET_KEY, settings.ALGORITHM).get(
            "sub"
        )
        assert user_id == user_id_from_token

    @staticmethod
    async def test_create_refresh_token():
        user_id = "1"
        refresh_token = await create_refresh_token(user_id)

        user = await UsersService.get_one_or_none(id=int(user_id))
        assert user

        token_id_from_table = user.refresh_token_id
        token_id_from_token = jwt.decode(
            refresh_token, settings.SECRET_KEY, settings.ALGORITHM
        ).get("token_id")
        assert token_id_from_table == token_id_from_token


# class TestsEmailService:

#     @staticmethod
#     async def test_create_unique_url():
#         url = create_unique_url()
#         assert settings.API_ADRESS in url

#     @staticmethod
#     async def test_create_message():
#         message_to = "test@example.com"
#         message = create_message_for_register(message_to)
#         assert message
#         assert message["From"] == settings.SMTP_USER
#         assert message["To"] == message_to
#         assert settings.API_ADRESS in message.get_content()
