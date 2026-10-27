from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main.api.configs.config import Config

# Создаем движок
engine = create_engine(
    Config.get("database_url"),
    echo=False  # True для отображения SQL-запросов в консоли
)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine)