import pytest
from src.main.api.models.user_models import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.db.crud.user_crud_db import UserCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCreateUser:

    @pytest.mark.parametrize("user_data", [RandomModelGenerator.generate(CreateUserRequest)])
    def test_create_user_valid(self, api_manager, db_session: Session, user_data):
        request_model = CreateUserRequest(**user_data)
        response = api_manager.admin.create_user(request_model)

        assert response.username == request_model.username, "Username в ответе не совпадает с отправленным"

        # Проверка в БД
        user_from_db = UserCrudDb.get_user_by_username(db_session, request_model.username)
        assert user_from_db is not None, "Пользователь создан, но его нет в БД!"
        assert user_from_db.username == request_model.username, "Username в БД не совпадает"

    @pytest.mark.parametrize("username, password", [
        ("абв", "ValidPass1!"), ("A", "ValidPass1!"), ("AB!", "ValidPass1!"),
        ("Max1", "Password"), ("Max2", "1234567"), ("Max3", "password1!"),
        ("Max4", "PASSWORD1!"), ("Max5", "Password"), ("Max6", "Password1"),
    ])
    def test_create_user_invalid(self, db_session: Session, username, password):
        request_model = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        requester = CrudRequester(
            RequestSpecs.auth_headers("admin", "123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.bad_request()
        )
        requester.post(request_model)

        # Проверка, что пользователь НЕ создался в БД
        user_from_db = UserCrudDb.get_user_by_username(db_session, username)
        assert user_from_db is None, f"Пользователь {username} не должен был создаться, но найден в БД!"