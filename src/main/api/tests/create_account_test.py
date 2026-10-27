import pytest
from src.main.api.db.crud.account_crud_db import AccountCrudDb
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCreateAccount:

    def test_create_account(self, api_manager, db_session: Session, create_user_request):
        # Создаем аккаунт через API
        response = api_manager.user.create_account(create_user_request)

        assert response.balance == 0, "Баланс нового аккаунта должен быть 0"

        # Проверка в БД
        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db is not None, f"Аккаунт с ID {response.id} не найден в БД!"
        assert account_from_db.balance is not None, "Поле баланса отсутствует в БД"