from pydantic import BaseModel as PydanticBaseModel, ConfigDict

class BaseModel(PydanticBaseModel):
    # Разрешает создавать модель как по имени поля (account_id), так и по алиасу (accountId)
    model_config = ConfigDict(populate_by_name=True)