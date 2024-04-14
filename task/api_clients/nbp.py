from typing import Optional

import requests

from task.logger import logger


class NBPApiClient:
    BASE_EXCHANGE_RATES_URL = "http://api.nbp.pl/api/exchangerates/rates/{}/{}"

    def _get_currency_rate(self, url: str) -> Optional[float]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            json_data = response.json()
            currency_rate = json_data["rates"][0]["mid"]
            return round(currency_rate, 2)
        except requests.exceptions.RequestException as e:
            logger.log_error(f"Failed to fetch data from API: {e}")
        except (KeyError, IndexError):
            logger.log_error("NBP API response structure has changed.")
        return None

    def get_latest_currency_rate(
        self, currency_code: str, table: str = "A"
    ) -> Optional[float]:
        today_exchange_rates_url = self.BASE_EXCHANGE_RATES_URL.format(
            table, currency_code
        )
        currency_rate = self._get_currency_rate(today_exchange_rates_url)
        if currency_rate is None:
            logger.log_info(
                "Most likely NBP has no currency rate for today."
                "The yesterday data will be uploaded."
            )
            yesterday_exchange_rates_url = today_exchange_rates_url.replace(
                "/today", ""
            )
            currency_rate = self._get_currency_rate(yesterday_exchange_rates_url)
        return currency_rate
