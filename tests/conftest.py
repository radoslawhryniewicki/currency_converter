import pytest

from task.models import ConvertedPricePLN, PriceConversionDetails


@pytest.fixture()
def price_conversion_details():
    return PriceConversionDetails(
        currency_code="EUR", source_price=1000.50, data_source="api"
    )


@pytest.fixture()
def converted_price():
    return ConvertedPricePLN(currency="EUR", rate=1000, price_in_pln=4400.0)
