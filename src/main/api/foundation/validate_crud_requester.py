import allure
from typing import Optional
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        requester = CrudRequester(self.headers, self.endpoint, self.response_spec)
        response = requester.post(model)

        # Получаем имя класса модели
        model_name = self.endpoint.value.response_model.__name__

        with allure.step(f"Validate response by model: {model_name}"):
            # Прикрепляем текстовую информацию о том, какая модель используется
            allure.attach(
                f"Validated model: {model_name}",
                name="Validation Model",
                attachment_type=allure.attachment_type.TEXT
            )
            return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int):
        requester = CrudRequester(self.headers, self.endpoint, self.response_spec)
        requester.delete(user_id)