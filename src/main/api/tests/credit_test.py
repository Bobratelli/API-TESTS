import random
import pytest
from src.main.api.models.transaction_models import CreditRequest, CreditRepayRequest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCredit:

    def test_credit_request_success(self, api_manager, db_session: Session, create_credit_user):
        account = api_manager.user.create_account(create_credit_user)

        amount = float(random.randint(5000, 15000))
        credit_model = CreditRequest(account_id=account.id, amount=amount, term_months=12)

        api_manager.user.request_credit(create_credit_user, credit_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == amount, "Баланс не пополнился на сумму кредита"

    def test_credit_request_forbidden_role(self, api_manager, create_user_request, create_account):
        amount = float(random.randint(5000, 15000))
        credit_model = CreditRequest(account_id=create_account.id, amount=amount, term_months=12)

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.forbidden()
        )
        requester.post(credit_model)

    def test_credit_repay_success(self, api_manager, db_session: Session, create_credit_user, credit_issued):
        account, credit_id, credit_amount = credit_issued

        repay_model = CreditRepayRequest(
            credit_id=credit_id,
            account_id=account.id,
            amount=credit_amount
        )

        api_manager.user.repay_credit(create_credit_user, repay_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == 0.0, "Баланс не уменьшился после погашения"

    def test_credit_repay_invalid_id(self, api_manager, create_credit_user, create_account):
        invalid_credit_id = random.randint(100000, 999999)
        amount = float(random.randint(5000, 15000))

        repay_model = CreditRepayRequest(
            credit_id=invalid_credit_id,
            account_id=create_account.id,
            amount=amount
        )

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_credit_user.username, create_credit_user.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.not_found()
        )
        requester.post(repay_model)