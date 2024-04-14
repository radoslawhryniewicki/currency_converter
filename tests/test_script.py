from unittest.mock import patch

import pytest

from script import (
    currency_converter,
    get_currency_rate_from_specified_data_source,
    save_to_db,
)


@patch("script.get_currency_rate_from_specified_data_source")
@patch("script.save_to_db")
def test_currency_converter_when_currency_rate_and_successfull_saved_to_db(
    mock_save_to_db,
    mock_currency_rate_from_data_source,
    caplog,
    price_conversion_details,
):
    mock_currency_rate_from_data_source.return_value = 4.33

    currency_converter(price_conversion_details, "dev")

    assert "Latest currency rate EUR/PLN: 4.33" in caplog.text


@patch("script.get_currency_rate_from_specified_data_source")
def test_currency_converter_when_no_currency_rate_from_data_source(
    mock_currency_rate_from_data_source,
    caplog,
    price_conversion_details,
):
    mock_currency_rate_from_data_source.return_value = None
    with pytest.raises(SystemExit):
        currency_converter(price_conversion_details, "dev")

    assert "Cannot get currency rate from specific data source." in caplog.text


@patch("script.JSONFileDatabaseConnector")
def test_save_to_db_successfull_in_dev_env(mock_file_db_conn, caplog, converted_price):
    mock_instance = mock_file_db_conn.return_value
    mock_instance.save.return_value = True

    save_to_db(converted_price, "dev")

    assert "The converted price details has been saved into dev database" in caplog.text


@patch("script.SQLiteConnector")
def test_save_to_db_successfull_in_prod_env(mock_sqlite_conn, caplog, converted_price):
    mock_instance = mock_sqlite_conn.return_value
    mock_instance.save.return_value = True

    save_to_db(converted_price, "prod")

    assert (
        "The converted price details has been saved into prod database" in caplog.text
    )



@patch("script.JSONRawFileConnector")
def test_get_currency_rate_from_json_data_source(
    mock_raw_file_conn, price_conversion_details
):
    mock_instance = mock_raw_file_conn.return_value
    mock_instance.get_currency_rate.return_value = 4.33
    price_conversion_details.data_source = "json"

    currency_rate = get_currency_rate_from_specified_data_source(
        price_conversion_details
    )
    assert currency_rate == 4.33


@patch("script.NBPApiClient")
def test_get_currency_rate_from_api_data_source(
    mock_nbp_api_client, price_conversion_details
):
    mock_instance = mock_nbp_api_client.return_value
    mock_instance.get_latest_currency_rate.return_value = 4.22
    currency_rate = get_currency_rate_from_specified_data_source(
        price_conversion_details
    )
    assert currency_rate == 4.22
