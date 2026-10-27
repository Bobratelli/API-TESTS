import pytest
from sqlalchemy import text
from src.main.api.db.models.engine import engine, SessionLocal
from src.main.api.classes.app_manager import AppManager
from src.main.api.models.user_models import CreateUserRequest, CreateUserResponse
from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.generators.model_generator import RandomModelGenerator


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
    # Генерируем уникальные данные и создаем пользователя (сохраняется в created_object)
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
    # 1. Генерируем и создаем пользователя (с ролью ROLE_USER)
    user_data = RandomModelGenerator.generate(CreateUserRequest)
    request_model = CreateUserRequest(**user_data)
    api_manager.admin.create_user(request_model)

    # 2. Открываем НОВУЮ сессию, чтобы изменения увидел API-сервер
    db = SessionLocal()
    try:
        db.execute(
            text('UPDATE "user" SET role = :role WHERE username = :username'),
            # Используем ROLE_CREDIT_SECRET из вашего файла требований!
            {"role": "ROLE_CREDIT_SECRET", "username": request_model.username}
        )
        db.commit()  # Фиксируем изменения навсегда (до очистки в teardown)
    finally:
        db.close()

    return request_model