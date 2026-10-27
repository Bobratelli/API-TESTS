from dataclasses import dataclass
from typing import Optional, Type
from enum import Enum
from src.main.api.models.base_model import BaseModel
from src.main.api.models.login_models import LoginUserRequest, LoginUserResponse
from src.main.api.models.user_models import CreateUserRequest, CreateUserResponse
from src.main.api.models.account_models import CreateAccountResponse
from src.main.api.models.transaction_models import (
    DepositRequest, TransferRequest, CreditRequest, CreditRepayRequest, TransactionResponse, CreditResponse
)

@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]] = None
    response_model: Optional[Type[BaseModel]] = None

class Endpoint(Enum):
    LOGIN_USER = EndpointConfiguration("/auth/token/login", LoginUserRequest, LoginUserResponse)
    ADMIN_CREATE_USER = EndpointConfiguration("/admin/create", CreateUserRequest, CreateUserResponse)
    ADMIN_DELETE_USER = EndpointConfiguration("/admin/users")
    CREATE_ACCOUNT = EndpointConfiguration("/account/create", None, CreateAccountResponse)
    DEPOSIT = EndpointConfiguration("/account/deposit", DepositRequest, TransactionResponse)
    TRANSFER = EndpointConfiguration("/account/transfer", TransferRequest, TransactionResponse)
    CREDIT_REQUEST = EndpointConfiguration("/credit/request", CreditRequest, CreditResponse)
    CREDIT_REPAY = EndpointConfiguration("/credit/repay", CreditRepayRequest, TransactionResponse)