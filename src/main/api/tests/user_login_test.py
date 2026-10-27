import pytest
from src.main.api.models.login_models import LoginUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator


@pytest.mark.api
class TestUserLogin:

    def test_login_admin(self, api_manager):
        request_model = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin.login_user(request_model)

        assert response.user.username == "admin"
        assert response.user.role == "ROLE_ADMIN"

    def test_login_user(self, api_manager, create_user_request):
        request_model = LoginUserRequest(
            username=create_user_request.username,
            password=create_user_request.password
        )
        response = api_manager.admin.login_user(request_model)

        assert response.user.username == create_user_request.username
        assert response.user.role == "ROLE_USER"