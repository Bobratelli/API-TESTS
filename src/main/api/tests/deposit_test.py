import random
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
        amount = float(random.randint(1000, 9000))
        deposit_model = DepositRequest(account_id=create_account.id, amount=amount)

        api_manager.user.deposit(create_user_request, deposit_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, create_account.id)
        assert account_from_db.balance == amount, "Баланс в БД не совпадает с суммой депозита"

    def test_deposit_invalid_account(self, create_user_request):
        invalid_account_id = random.randint(100000, 999999)
        amount = float(random.randint(1000, 9000))
        deposit_model = DepositRequest(account_id=invalid_account_id, amount=amount)

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.not_found()
        )
        requester.post(deposit_model)