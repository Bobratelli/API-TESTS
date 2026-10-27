from pathlib import Path
from typing import Any, Dict


class Config:
    _instance = None
    _dictionary: Dict[str, str] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            current_path = Path(__file__).resolve()
            root_path = current_path.parent
            while not (root_path / "resources").exists() and root_path != root_path.parent:
                root_path = root_path.parent

            config_path = root_path / "resources" / "urls.properties"

            if not config_path.exists():
                raise FileNotFoundError(f"Файл конфигурации не найден по пути: {config_path}")

            with open(config_path, "r", encoding="utf-8") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        cls._dictionary[key.strip()] = value.strip()
        return cls._instance

    @classmethod
    def get(cls, key: str, default_value: Any = None) -> Any:
        cls()
        return cls._dictionary.get(key, default_value)