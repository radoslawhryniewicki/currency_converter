from unittest.mock import patch

import pytest

from task.connectors.database.json import JSONFileDatabaseConnector


@pytest.fixture
def json_db_data() -> dict:
    return {
        "1": {
            "id": 1,
            "currency": "eur",
            "rate": 4.6285,
            "price_in_pln": 21.1,
            "date": "2010-01-01",
        },
        "3": {
            "id": 3,
            "currency": "eur",
            "rate": 4.985,
            "price_in_pln": 22.1,
            "date": "2012-01-01",
        },
    }


class TestJSONFileDatabaseConnector:
    @patch("task.connectors.database.json.JSONFileDatabaseConnector._read_data")
    def test_get_next_id(self, mock_data, json_db_data):
        mock_data.return_value = json_db_data
        conn = JSONFileDatabaseConnector()
        assert conn._get_next_id() == "2"

        json_db_data.update(
            {
                "2": {
                    "id": 2,
                    "currency": "eur",
                    "rate": 4.975,
                    "price_in_pln": 22.5,
                    "date": "2012-01-02",
                }
            }
        )
        assert conn._get_next_id() == "4"