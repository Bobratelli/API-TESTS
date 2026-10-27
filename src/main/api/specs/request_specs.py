import requests
from src.main.api.configs.config import Config
from src.main.api.models.login_models import LoginUserRequest


class RequestSpecs:
    @staticmethod
    def headers() -> dict:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> dict:
        url = f"{Config.get('backend').rstrip('/')}/auth/token/login"
        login_request = LoginUserRequest(username=username, password=password)
        response = requests.post(url, json=login_request.model_dump(), headers=RequestSpecs.headers())

        if response.status_code == 200:
            token = response.json().get("token")
            headers = RequestSpecs.headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        raise Exception(f"Failed to authorize user {username}: {response.text}")

    @staticmethod
    def base_url() -> str:
        return Config.get("backend")