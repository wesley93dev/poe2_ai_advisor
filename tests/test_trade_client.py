import pytest
from core.trade_client import TradeClient
from core.payload_builder import PayloadBuilder

def test_trade_client_fetch_prices(monkeypatch):
    # Mock da resposta da API
    class MockResponse:
        def __init__(self, json_data):
            self._json = json_data
        def json(self): return self._json
        def raise_for_status(self): pass

    def mock_post(url, json, timeout):
        return MockResponse({"id": "123", "result": ["abc123", "def456"]})

    def mock_get(url, timeout):
        return MockResponse({
            "result": [
                {"item": {"name": "Iron Ring", "typeLine": "Ring"},
                 "listing": {"price": {"amount": 5, "currency": "chaos"}}}
            ]
        })

    monkeypatch.setattr("requests.post", mock_post)
    monkeypatch.setattr("requests.get", mock_get)

    client = TradeClient()
    payload = PayloadBuilder.for_rings_with_chaos()
    prices = client.fetch_prices(payload)

    assert len(prices) == 1
    assert prices[0]["price"] == 5
    assert prices[0]["currency"] == "chaos"
