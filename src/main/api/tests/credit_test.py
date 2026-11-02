import pytest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCredit:

    def test_credit_request_success(self, api_manager, db_session: Session, create_credit_user, valid_credit_data):
        credit_model, amount, account = valid_credit_data
        api_manager.user.request_credit(create_credit_user, credit_model)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)

        assert account_from_db.balance == amount, "Баланс не пополнился на сумму кредита"

    def test_credit_request_forbidden_role(self, create_user_request, forbidden_credit_data):
        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.forbidden()
        )
        requester.post(forbidden_credit_data)

    def test_credit_repay_success(self, api_manager, db_session: Session, create_credit_user, valid_repay_data):
        repay_model, account = valid_repay_data
        api_manager.user.repay_credit(create_credit_user, repay_model)
        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)

        assert account_from_db.balance == 0.0, "Баланс не уменьшился после погашения"

    def test_credit_repay_invalid_id(self, create_credit_user, invalid_repay_data):
        requester = CrudRequester(
            RequestSpecs.auth_headers(create_credit_user.username, create_credit_user.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.not_found()
        )
        requester.post(invalid_repay_data)