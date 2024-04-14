from .models import ConvertedPricePLN, PriceConversionDetails


class PriceCurrencyConverterToPLN:
    def __init__(
        self, conversion_details: PriceConversionDetails, currency_rate: float
    ) -> None:
        self.conversion_details = conversion_details
        self.currency_rate = currency_rate

    def convert_to_pln(self) -> ConvertedPricePLN:
        return ConvertedPricePLN(
            currency=self.conversion_details.currency_code,
            rate=self.currency_rate,
            price_in_pln=round(
                self.conversion_details.source_price * self.currency_rate,
                2,
            ),
        )
