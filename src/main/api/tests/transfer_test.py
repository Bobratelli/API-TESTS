import random
import pytest
from src.main.api.models.transaction_models import TransferRequest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestTransfer:

    def test_transfer_success(self, api_manager, db_session: Session, create_user_request, two_accounts_with_deposit):
        acc_from, acc_to, balance = two_accounts_with_deposit
        max_transfer = min(10000, int(balance))
        amount = float(random.randint(500, max_transfer))

        transfer_model = TransferRequest(
            from_account_id=acc_from.id,
            to_account_id=acc_to.id,
            amount=amount
        )

        api_manager.user.transfer(create_user_request, transfer_model)

        db_from = AccountCrudDb.get_account_by_id(db_session, acc_from.id)
        db_to = AccountCrudDb.get_account_by_id(db_session, acc_to.id)

        assert db_from.balance == (balance - amount), "Неверный баланс отправителя"
        assert db_to.balance == amount, "Неверный баланс получателя"

    def test_transfer_insufficient_funds(self, api_manager, create_user_request, create_account):
        account2 = api_manager.user.create_account(create_user_request)
        amount = float(random.randint(500, 10000))
        transfer_model = TransferRequest(
            from_account_id=create_account.id,
            to_account_id=account2.id,
            amount=amount
        )

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.unprocessable_entity()
        )
        requester.post(transfer_model)