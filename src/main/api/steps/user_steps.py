from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.validate_crud_requester import ValidateCrudRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.models.login_models import LoginUserRequest, LoginUserResponse
from src.main.api.models.account_models import CreateAccountResponse
from src.main.api.models.user_models import CreateUserRequest
from src.main.api.models.transaction_models import DepositRequest, TransferRequest, CreditRequest, CreditRepayRequest

class UserSteps(BaseSteps):
    def create_account(self, user_request: CreateUserRequest) -> CreateAccountResponse:
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers(user_request.username, user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.created()
        )
        return requester.post() # Тело не нужно

    def deposit(self, user_request: CreateUserRequest, deposit_request: DepositRequest):
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers(user_request.username, user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.request_ok()
        )
        return requester.post(deposit_request)

    def transfer(self, user_request: CreateUserRequest, transfer_request: TransferRequest):
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers(user_request.username, user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.request_ok()
        )
        return requester.post(transfer_request)

    def request_credit(self, user_request: CreateUserRequest, credit_request: CreditRequest):
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers(user_request.username, user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.created()
        )
        return requester.post(credit_request)

    def repay_credit(self, user_request: CreateUserRequest, repay_request: CreditRepayRequest):
        requester = ValidateCrudRequester(
            RequestSpecs.auth_headers(user_request.username, user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.request_ok()
        )
        return requester.post(repay_request)