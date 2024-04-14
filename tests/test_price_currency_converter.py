from task.price_currency_converter import PriceCurrencyConverterToPLN


class TestPriceCurrencyConverterToPLN:
    def test_convert_to_pln(self, price_conversion_details):
        converter = PriceCurrencyConverterToPLN(
            conversion_details=price_conversion_details,
            currency_rate=2.23,
        )

        converted_price_obj = converter.convert_to_pln()

        assert converted_price_obj.currency == price_conversion_details.currency_code
        assert converted_price_obj.rate == 2.23
        assert converted_price_obj.price_in_pln == 2231.11
