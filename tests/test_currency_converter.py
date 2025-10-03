import pytest
from core.currency_converter import CurrencyConverter

def test_currency_to_chaos():
    assert CurrencyConverter.to_chaos(1, "chaos") == 1
    assert CurrencyConverter.to_chaos(2, "divine") == 360
    assert CurrencyConverter.to_chaos(3, "exalted") == 150

def test_invalid_currency():
    with pytest.raises(ValueError):
        CurrencyConverter.to_chaos(1, "gold")
