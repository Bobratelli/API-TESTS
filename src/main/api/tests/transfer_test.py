import pytest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestTransfer:

    def test_transfer_success(self, api_manager, db_session: Session, create_user_request, valid_transfer_data):
        transfer_model, initial_balance, acc_from, acc_to = valid_transfer_data
        api_manager.user.transfer(create_user_request, transfer_model)
        db_from = AccountCrudDb.get_account_by_id(db_session, acc_from.id)
        db_to = AccountCrudDb.get_account_by_id(db_session, acc_to.id)

        assert db_from.balance == (initial_balance - transfer_model.amount), "Неверный баланс отправителя"
        assert db_to.balance == transfer_model.amount, "Неверный баланс получателя"

    def test_transfer_insufficient_funds(self, create_user_request, insufficient_transfer_data):
        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.TRANSFER,
            ResponseSpecs.unprocessable_entity()
        )
        requester.post(insufficient_transfer_data)