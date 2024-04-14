from unittest.mock import patch

import pytest
from freezegun import freeze_time

from task.connectors.local.file_reader import JSONRawFileConnector


@pytest.fixture
def json_data() -> dict:
    return {
        "USD": [
            {"date": "2024-04-14", "rate": 4.20},
            {"date": "2024-04-13", "rate": 4.22},
        ],
        "EUR": [
            {"date": "2024-04-13", "rate": 3.22},
            {"date": "2024-04-14", "rate": 3.20},
        ],
    }


class TestJSONRawFileConnector:
    @freeze_time("2024-04-13")
    @patch("task.connectors.local.file_reader.JSONRawFileConnector._read_data")
    def test_get_currency_data_when_actual_data_exists(self, mock_data, json_data):
        mock_data.return_value = json_data
        conn = JSONRawFileConnector()
        assert conn.get_currency_rate("USD") == 4.22

    @freeze_time("2024-04-11")
    @patch("task.connectors.local.file_reader.JSONRawFileConnector._read_data")
    def test_get_currency_data_when_actual_data_not_exists(self, mock_data, json_data):
        mock_data.return_value = json_data
        conn = JSONRawFileConnector()
        assert conn.get_currency_rate("USD") is None

    @freeze_time("2024-04-13")
    @patch("task.connectors.local.file_reader.JSONRawFileConnector._read_data")
    def test_get_currency_data_when_currency_not_exists(self, mock_data, json_data):
        mock_data.return_value = json_data
        conn = JSONRawFileConnector()
        assert conn.get_currency_rate("NOK") is None
