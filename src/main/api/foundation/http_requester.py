from typing import Callable
from src.main.api.foundation.endpoint import Endpoint

class HttpRequester:
    def __init__(self, request_spec: dict, endpoint: Endpoint, response_spec: Callable):
        self.headers = request_spec
        self.endpoint = endpoint
        self.response_spec = response_spec