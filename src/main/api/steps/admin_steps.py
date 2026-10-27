from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.user_models import CreateUserRequest, CreateUserResponse
from src.main.api.models.login_models import LoginUserRequest, LoginUserResponse

class AdminSteps(BaseSteps):
    def create_user(self, model: CreateUserRequest) -> CreateUserResponse:
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers("admin", "123456"),
            Endpoint.ADMIN_CREATE_USER,
            ResponseSpecs.request_ok()
        )
        response = requester.post(model)
        self.created_object.append(response)
        return response

    def delete_user(self, user_id: int):
        requester = CrudRequester(
            RequestSpecs.auth_headers("admin", "123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.request_ok()
        )
        requester.delete(user_id)

    def login_user(self, model: LoginUserRequest) -> LoginUserResponse:
        requester = ValidateCrudRequester(
            RequestSpecs.headers(),
            Endpoint.LOGIN_USER,
            ResponseSpecs.request_ok()
        )
        return requester.post(model)