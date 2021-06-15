from pydantic import BaseModel


class ExchangeRate(BaseModel):
    currency_from: str
    currency_to: str
    value: float
