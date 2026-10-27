import pytest
from src.main.api.models.transaction_models import TransferRequest, DepositRequest
from src.main.api.models.user_models import CreateUserRequest
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestTransfer:

    def test_transfer_success(self, api_manager, db_session: Session, create_user_request, create_account):
        user2_data = RandomModelGenerator.generate(CreateUserRequest)
        user2_req = CreateUserRequest(**user2_data)
        api_manager.admin.create_user(user2_req)
        account2 = api_manager.user.create_account(user2_req)

        # Пополняем первый счет (Сумма от 1000 до 9000)
        api_manager.user.deposit(create_user_request, DepositRequest(account_id=create_account.id, amount=2000.0))

        # Перевод (Сумма от 500 до 10000)
        transfer_sum = 500.0
        transfer_model = TransferRequest(
            from_account_id=create_account.id,
            to_account_id=account2.id,
            amount=transfer_sum
        )
        api_manager.user.transfer(create_user_request, transfer_model)

        acc1_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)
        acc2_db = AccountCrudDb.get_account_by_id(db_session, account2.id)

        assert acc1_db.balance == (2000.0 - transfer_sum), "Неверный баланс отправителя"
        assert acc2_db.balance == transfer_sum, "Неверный баланс получателя"

    def test_transfer_insufficient_funds(self, api_manager, create_user_request, create_account):
        # Создаем второй счет с балансом 0
        account2 = api_manager.user.create_account(create_user_request)

        # Пытаемся перевести 500, хотя на счете 0
        transfer_model = TransferRequest(
            from_account_id=create_account.id,
            to_account_id=account2.id,
            amount=500.0
        )

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.unprocessable_entity()
        )
        requester.post(transfer_model)