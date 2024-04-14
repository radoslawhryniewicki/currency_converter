import argparse
import sys
from typing import Optional

from pydantic import ValidationError

from task.api_clients.nbp import NBPApiClient
from task.connectors.database.json import JSONFileDatabaseConnector
from task.connectors.database.sqlite import SQLiteConnector
from task.connectors.local.file_reader import JSONRawFileConnector
from task.enums import DataSource, Environment
from task.logger import logger
from task.models import ConvertedPricePLN
from task.price_currency_converter import (PriceConversionDetails,
                                           PriceCurrencyConverterToPLN)


def get_currency_rate_from_specified_data_source(
    conversion_details: PriceConversionDetails,
) -> Optional[float]:
    if conversion_details.data_source == DataSource.JSON.value:
        return JSONRawFileConnector().get_currency_rate(
            conversion_details.currency_code
        )
    elif conversion_details.data_source == DataSource.API.value:
        return NBPApiClient().get_latest_currency_rate(conversion_details.currency_code)


def save_to_db(converted_price: ConvertedPricePLN, env) -> None:
    if env == Environment.DEV.value:
        file_db_conn = JSONFileDatabaseConnector()
        file_db_conn.save(entity=converted_price)
    else:
        sqlite_db_conn = SQLiteConnector()
        sqlite_db_conn.save(entity=converted_price)

    logger.log_info(f"The converted price details has been saved into {env} database")


def currency_converter(conversion_details: PriceConversionDetails, env: str) -> None:
    currency_rate = get_currency_rate_from_specified_data_source(conversion_details)
    if not currency_rate:
        logger.log_error("Cannot get currency rate from specific data source.")
        sys.exit()

    price_currency_converter = PriceCurrencyConverterToPLN(
        conversion_details, currency_rate
    )
    converted_price = price_currency_converter.convert_to_pln()
    logger.log_info(
        f"Latest currency rate {conversion_details.currency_code}/PLN: {currency_rate}"
    )
    save_to_db(converted_price, env)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is your currency converter.")
    parser.add_argument(
        "--env",
        choices=["dev", "prod"],
        help="Define environment. Choose between 'dev' or 'prod'. Default set as 'dev'",
        default="dev",
    )
    args = parser.parse_args()

    while True:
        source_price = input("Enter the source price in float format: ")
        currency_code = input(
            "Enter 3-char currency code in ISO 4217 format which has to be converted e.g. EUR: "
        )
        data_source = input("Enter 'api' or 'json' to choose data source: ")
        try:
            conversion_details = PriceConversionDetails(
                currency_code=currency_code,
                source_price=source_price,
                data_source=data_source,
            )
            break
        except ValidationError as e:
            print(e)
            continue

    currency_converter(conversion_details, args.env)
