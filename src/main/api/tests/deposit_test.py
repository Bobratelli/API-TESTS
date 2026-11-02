import pytest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestDeposit:

    def test_deposit_success(self, api_manager, db_session: Session, create_user_request, valid_deposit_data):
        deposit_model, amount = valid_deposit_data
        api_manager.user.deposit(create_user_request, deposit_model)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, deposit_model.account_id)

        assert account_from_db.balance == amount, "Баланс в БД не совпадает с суммой депозита"

    def test_deposit_invalid_account(self, create_user_request, invalid_deposit_data):
        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.DEPOSIT,
            ResponseSpecs.not_found()
        )
        requester.post(invalid_deposit_data)