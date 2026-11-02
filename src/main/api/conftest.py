import pytest
import random
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.main.api.models.transaction_models import CreditRequest, DepositRequest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from src.main.api.db.models.engine import engine, SessionLocal
from src.main.api.classes.app_manager import AppManager
from src.main.api.models.user_models import CreateUserRequest, CreateUserResponse
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.transaction_models import (
    DepositRequest, TransferRequest, CreditRequest, CreditRepayRequest
)


@pytest.fixture
def created_object():
    objects = []
    yield objects

    # Очистка после теста
    admin_steps = AdminSteps([])
    for obj in objects:
        if isinstance(obj, CreateUserResponse):
            try:
                admin_steps.delete_user(obj.id)
            except Exception as e:
                print(f"Error deleting user {obj.id}: {e}")


@pytest.fixture
def api_manager(created_object):
    return AppManager(created_object)


@pytest.fixture
def create_user_request(api_manager):
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    request_model = CreateUserRequest(**user_data)
    api_manager.admin.create_user(request_model)
    return request_model


@pytest.fixture
def db_session():
    # 1. Подключаемся к базе
    connection = engine.connect()
    # 2. Начинаем транзакцию
    transaction = connection.begin()
    # 3. Создаем сессию, привязанную к этому соединению
    session = SessionLocal(bind=connection)

    yield session

    # 4. После теста всё откатываем и закрываем
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def create_account(api_manager, create_user_request):
    """Создает счет для пользователя и возвращает ответ с ID счета"""
    response = api_manager.user.create_account(create_user_request)
    return response


@pytest.fixture
def create_credit_user(api_manager):
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    request_model = CreateUserRequest(**user_data)
    api_manager.admin.create_user(request_model)

    db = SessionLocal()
    try:
        db.execute(
            text('UPDATE "user" SET role = :role WHERE username = :username'),
            {"role": "ROLE_CREDIT_SECRET", "username": request_model.username}
        )
        db.commit()
    finally:
        db.close()

    return request_model


@pytest.fixture
def deposited_account(api_manager, create_user_request, create_account):
    """Создает счет и пополняет его на случайную сумму (1000 - 9000)"""
    amount = random.randint(1000, 9000)
    deposit_model = DepositRequest(account_id=create_account.id, amount=float(amount))
    api_manager.user.deposit(create_user_request, deposit_model)
    return create_account, float(amount)


@pytest.fixture
def two_accounts_with_deposit(api_manager, create_user_request, deposited_account):
    """Возвращает два счета: первый (уже пополненный) и второй (пустой)"""
    first_account, balance = deposited_account
    second_account = api_manager.user.create_account(create_user_request)
    return first_account, second_account, balance


@pytest.fixture
def credit_issued(api_manager, create_credit_user):
    """
    Предусловие для тестов погашения:
    Создает кредитному юзеру счет и сразу оформляет на него кредит.
    Возвращает кортеж: (аккаунт, ID кредита, сумма кредита)
    """
    account = api_manager.user.create_account(create_credit_user)
    amount = float(random.randint(5000, 15000))

    credit_model = CreditRequest(
        account_id=account.id,
        amount=amount,
        term_months=12
    )
    response = api_manager.user.request_credit(create_credit_user, credit_model)
    return account, response.credit_id, amount


@pytest.fixture
def valid_deposit_data(api_manager, create_user_request, create_account):
    amount = float(random.randint(1000, 9000))
    model = DepositRequest(account_id=create_account.id, amount=amount)
    return model, amount


@pytest.fixture
def invalid_deposit_data():
    invalid_id = random.randint(100000, 999999)
    amount = float(random.randint(1000, 9000))
    return DepositRequest(account_id=invalid_id, amount=amount)


@pytest.fixture
def valid_transfer_data(two_accounts_with_deposit):
    acc_from, acc_to, initial_balance = two_accounts_with_deposit
    max_transfer = min(10000, int(initial_balance))
    amount = float(random.randint(500, max_transfer))

    model = TransferRequest(
        from_account_id=acc_from.id,
        to_account_id=acc_to.id,
        amount=amount
    )
    return model, initial_balance, acc_from, acc_to


@pytest.fixture
def insufficient_transfer_data(api_manager, create_user_request, create_account):
    acc_to = api_manager.user.create_account(create_user_request)
    amount = float(random.randint(500, 10000))

    model = TransferRequest(
        from_account_id=create_account.id,
        to_account_id=acc_to.id,
        amount=amount
    )
    return model


@pytest.fixture
def valid_credit_data(api_manager, create_credit_user):
    account = api_manager.user.create_account(create_credit_user)
    amount = float(random.randint(5000, 15000))
    model = CreditRequest(account_id=account.id, amount=amount, term_months=12)
    return model, amount, account


@pytest.fixture
def forbidden_credit_data(api_manager, create_user_request):
    # Обычный юзер с обычным счетом
    account = api_manager.user.create_account(create_user_request)
    amount = float(random.randint(5000, 15000))
    return CreditRequest(account_id=account.id, amount=amount, term_months=12)


@pytest.fixture
def valid_repay_data(credit_issued):
    # credit_issued возвращает (account, credit_id, amount)
    account, credit_id, amount = credit_issued
    model = CreditRepayRequest(
        credit_id=credit_id,
        account_id=account.id,
        amount=amount
    )
    return model, account


@pytest.fixture
def invalid_repay_data(api_manager, create_credit_user):
    account = api_manager.user.create_account(create_credit_user)
    amount = 5000.0
    deposit_model = DepositRequest(account_id=account.id, amount=amount)
    api_manager.user.deposit(create_credit_user, deposit_model)

    invalid_id = random.randint(100000, 999999)
    return CreditRepayRequest(
        credit_id=invalid_id,
        account_id=account.id,
        amount=amount
    )