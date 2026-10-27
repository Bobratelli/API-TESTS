from src.main.api.models.base_model import BaseModel

class LoginUserRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    username: str
    role: str

class LoginUserResponse(BaseModel):
    token: str
    user: User