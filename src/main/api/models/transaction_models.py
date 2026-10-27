from pydantic import Field
from src.main.api.models.base_model import BaseModel

class DepositRequest(BaseModel):
    account_id: int = Field(alias="accountId", gt=0)
    amount: float = Field(ge=1000, le=9000)

class TransferRequest(BaseModel):
    from_account_id: int = Field(alias="fromAccountId", gt=0)
    to_account_id: int = Field(alias="toAccountId", gt=0)
    amount: float = Field(ge=500, le=10000)

class CreditRequest(BaseModel):
    account_id: int = Field(alias="accountId", gt=0)
    amount: float = Field(ge=5000, le=15000)
    term_months: int = Field(alias="termMonths", ge=1, le=60)

class CreditRepayRequest(BaseModel):
    credit_id: int = Field(alias="creditId", gt=0)
    account_id: int = Field(alias="accountId", gt=0)
    amount: float = Field(gt=0)

class CreditResponse(BaseModel):
    id: int
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")

class TransactionResponse(BaseModel):
    message: str | None = None
    status: str | None = None