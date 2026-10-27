from typing import Protocol, Optional
from src.main.api.models.base_model import BaseModel

class CrudEndpoint(Protocol):
    def post(self, model: Optional[BaseModel] = None) -> dict | BaseModel:
        ...
    def delete(self, user_id: int) -> dict | BaseModel:
        ...