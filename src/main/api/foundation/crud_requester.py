import requests
import allure
from typing import Optional
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.crud_endpoint import CrudEndpoint
from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel


class CrudRequester(HttpRequester, CrudEndpoint):
    def post(self, model: Optional[BaseModel] = None) -> requests.Response:
        url = f"{Config.get('backend').rstrip('/')}{self.endpoint.value.url}"
        body = model.model_dump(by_alias=True) if model else None

        # Allure с динамическим названием
        with allure.step(f"POST {url}"):
            if body:
                allure.attach(
                    str(body),
                    name="Request Body",
                    attachment_type=allure.attachment_type.JSON
                )

            response = requests.post(url=url, json=body, headers=self.headers)

            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )

            self.response_spec(response)
            return response

    def delete(self, user_id: int) -> requests.Response:
        url = f"{Config.get('backend').rstrip('/')}{self.endpoint.value.url}/{user_id}"

        with allure.step(f"DELETE {url}"):
            response = requests.delete(url=url, headers=self.headers)

            if response.text:
                allure.attach(
                    response.text,
                    name="Response Body",
                    attachment_type=allure.attachment_type.JSON
                )

            self.response_spec(response)
            return response