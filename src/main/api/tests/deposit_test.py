import pytest
from src.main.api.models.transaction_models import DepositRequest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestDeposit:

    def test_deposit_success(self, api_manager, db_session: Session, create_user_request, create_account):
        # Сумма от 1000 до 9000
        amount = 1500.0
        deposit_model = DepositRequest(account_id=create_account.id, amount=amount)

        api_manager.user.deposit(create_user_request, deposit_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)

        assert account_from_db is not None, "Счет не найден в БД"
        assert account_from_db.balance == amount, f"Баланс в БД {account_from_db.balance} не совпадает с ожидаемым {amount}"

    def test_deposit_invalid_account(self, create_user_request):
        deposit_model = DepositRequest(account_id=999999, amount=1500.0)

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.not_found()
        )
        requester.post(deposit_model)