import pytest

from task.models import PriceConversionDetails


def test_invalid_currency_code_raise_exc():
    with pytest.raises(ValueError):
        PriceConversionDetails(
            currency_code="AAA", source_price=1000.50, data_source="api"
        )


def test_invalid_source_price_raise_exc():
    with pytest.raises(ValueError):
        PriceConversionDetails(
            currency_code="USD", source_price="10.r", data_source="api"
        )


def test_invalid_data_source_raise_exc():
    with pytest.raises(ValueError):
        PriceConversionDetails(
            currency_code="USD", source_price="10.55", data_source="sth"
        )
