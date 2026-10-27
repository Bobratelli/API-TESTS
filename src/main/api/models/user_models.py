from typing import Annotated
from src.main.api.models.base_model import BaseModel
from src.main.api.generators.creation_rule import CreationRule

class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(rx=r"^[a-zA-Z0-9]{3,15}$")]
    password: Annotated[str, CreationRule(rx=r"^[A-Z]{3}[a-z]{1}[0-9]{2}[!@#$%^&*]{4}$")]
    role: Annotated[str, CreationRule(rx=r"^ROLE_USER$")]

class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str