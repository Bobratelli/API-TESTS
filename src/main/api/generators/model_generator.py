import random
import string
from typing import Any, get_origin, get_args, get_type_hints, Annotated
from pydantic import BaseModel
from rstr import xeger
from src.main.api.generators.creation_rule import CreationRule


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type[BaseModel]) -> Any:
        """Генерирует словарь данных на основе аннотаций и типов полей модели"""
        type_hints = get_type_hints(cls, include_extras=True)
        data = {}

        for field_name, field_type in type_hints.items():
            actual_type = field_type
            has_rule = False
            rule = None

            # Проверяем, есть ли Annotated и CreationRule
            if get_origin(field_type) is Annotated:
                args = get_args(field_type)
                actual_type = args[0]
                for arg in args[1:]:
                    if isinstance(arg, CreationRule):
                        has_rule = True
                        rule = arg
                        break

            # Если есть правило, генерируем по регулярке
            if has_rule:
                value = RandomModelGenerator._generate_from_regex(rule.rx, actual_type)
            else:
                # Иначе генерируем по типу
                value = RandomModelGenerator._generate_value(actual_type)

            data[field_name] = value

        return data

    @staticmethod
    def _generate_from_regex(rx: str, field_type: type) -> Any:
        generated = xeger(rx)
        if field_type is int:
            return int(generated)
        if field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if field_type is int:
            return random.randint(1, 999)
        if field_type is float:
            return round(random.uniform(0.0, 1000.0), 2)
        if field_type is bool:
            return random.choice([True, False])
        if field_type is list:
            return [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(5)]

        # Если это вложенная Pydantic модель (рекурсия)
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            return RandomModelGenerator.generate(field_type)

        return None