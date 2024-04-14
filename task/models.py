from datetime import datetime

from currencies import Currency
from currencies.exceptions import CurrencyDoesNotExist
from pydantic import BaseModel, field_validator


class PriceConversionDetails(BaseModel):
    currency_code: str
    source_price: float
    data_source: str

    @field_validator("currency_code")
    def validate_currency_code(cls, v):
        v = v.upper()
        try:
            Currency(v)
        except CurrencyDoesNotExist:
            raise ValueError(
                "Currency does not exist. Ensure you write proper currency."
            )
        return v

    @field_validator("data_source")
    def validate_data_source(cls, v):
        v = v.lower()
        if v not in ["api", "json"]:
            raise ValueError("Field must be 'api' or 'json'")
        return v


class ConvertedPricePLN(BaseModel):
    currency: str
    rate: float
    price_in_pln: float
    date: str = datetime.now().strftime("%Y-%m-%d")
