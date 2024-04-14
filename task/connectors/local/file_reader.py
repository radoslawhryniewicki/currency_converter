# TODO connector for reading local source (example_currency_rates.json) with currency rates
import json
from datetime import datetime
from typing import Optional

from task.config import JSON_EXAMPLE_CURRENCY_RATES

# now_datetime = datetime.now().strftime("%Y-%m-%d")


class JSONRawFileConnector:
    def __init__(self) -> None:
        self._data = self._read_data()

    @staticmethod
    def _read_data() -> dict:
        with open(JSON_EXAMPLE_CURRENCY_RATES, "r") as file:
            return json.load(file)

    def get_currency_rate(self, currency: str) -> Optional[str]:
        currency_data = self._data.get(currency)
        if currency_data:
            for data in currency_data:
                if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                    return data.get("rate")
