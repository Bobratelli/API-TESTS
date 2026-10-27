from typing import Callable
import requests

class ResponseSpecs:
    @staticmethod
    def request_ok() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 200, response.text
        return confirm

    @staticmethod
    def created() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 201, response.text
        return confirm

    @staticmethod
    def bad_request() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 400, response.text
        return confirm

    @staticmethod
    def forbidden() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 403, response.text

        return confirm

    @staticmethod
    def not_found() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 404, response.text

        return confirm

    @staticmethod
    def unprocessable_entity() -> Callable:
        def confirm(response: requests.Response):
            assert response.status_code == 422, response.text

        return confirm