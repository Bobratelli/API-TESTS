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

        credit_amount = 5000.0
        credit_model = CreditRequest(
            account_id=account.id,
            amount=credit_amount,
            term_months=12
        )

        response = api_manager.user.request_credit(create_credit_user, credit_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == credit_amount, "Баланс не пополнился на сумму кредита"

    def test_credit_request_forbidden_role(self, api_manager, create_user_request):
        account = api_manager.user.create_account(create_user_request)

        credit_model = CreditRequest(
            account_id=account.id,
            amount=5000.0,
            term_months=12
        )

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.forbidden()
        )
        requester.post(credit_model)

    def test_credit_repay_success(self, api_manager, db_session: Session, create_credit_user):
        account = api_manager.user.create_account(create_credit_user)
        credit_amount = 5000.0
        credit_model = CreditRequest(account_id=account.id, amount=credit_amount, term_months=6)

        # Берем ID кредита из ответа сервера
        response = api_manager.user.request_credit(create_credit_user, credit_model)
        credit_id = response.credit_id

        # Погашаем кредит
        repay_model = CreditRepayRequest(
            credit_id=credit_id,
            account_id=account.id,
            amount=credit_amount
        )
        api_manager.user.repay_credit(create_credit_user, repay_model)

        account_from_db = AccountCrudDb.get_account_by_id(db_session, account.id)
        assert account_from_db.balance == 0.0, "Баланс не уменьшился после погашения"

    def test_credit_repay_invalid_id(self, api_manager, create_user_request, create_account):
        # Пытаемся погасить кредит, которого не существует
        repay_model = CreditRepayRequest(
            credit_id=999999,
            account_id=create_account.id,
            amount=5000.0
        )

        requester = CrudRequester(
            RequestSpecs.auth_headers(create_user_request.username, create_user_request.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.forbidden()
        )
        requester.post(repay_model)