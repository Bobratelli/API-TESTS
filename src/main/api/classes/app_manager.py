from src.main.api.steps.admin_steps import AdminSteps
from src.main.api.steps.user_steps import UserSteps

class AppManager:
    def __init__(self, created_object: list):
        self.admin = AdminSteps(created_object)
        self.user = UserSteps(created_object)