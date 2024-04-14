from unittest.mock import patch

import pytest
from requests import HTTPError

from task.api_clients.nbp import NBPApiClient


@pytest.fixture
def nbp_client():
    return NBPApiClient()


class TestNBPApiClient:
    @patch("requests.get")
    def test_get_latest_currency_rate_exists(self, mock_get, nbp_client):
        mock_instance = mock_get.return_value
        mock_instance.status_code = 200
        mock_instance.json.return_value = {
            "rates": [{"mid": 4.3376}],
        }

        currency_rate = nbp_client.get_latest_currency_rate("EUR")

        assert currency_rate == 4.34

    @patch("requests.get")
    def test_get_latest_currency_rate_return_different_status_code_from_response(
        self, mock_get, caplog, nbp_client
    ):
        mock_get.side_effect = HTTPError

        currency_rate = nbp_client.get_latest_currency_rate("EUR")

        assert currency_rate is None
        assert "Failed to fetch data from API" in caplog.text

    @patch("requests.get")
    def test_get_latest_currency_rate_return_response_with_different_structure(
        self, mock_get, caplog, nbp_client
    ):
        mock_instance = mock_get.return_value
        mock_instance.status_code = 200
        mock_instance.json.return_value = {
            "rates": {"mid": 4.3376},
        }

        currency_rate = nbp_client.get_latest_currency_rate("EUR")

        assert currency_rate is None
        assert "NBP API response structure has changed." in caplog.text

    @patch.object(NBPApiClient, "_get_currency_rate")
    def test_get_latest_currency_rate_return_yesterday_currency_rate(
        self, mock_get_currency_rate, caplog, nbp_client
    ):
        mock_get_currency_rate.side_effect = [None, 4.22]

        currency_rate = nbp_client.get_latest_currency_rate("EUR")

        assert currency_rate == 4.22
        assert "Most likely NBP has no currency rate for today." in caplog.text
