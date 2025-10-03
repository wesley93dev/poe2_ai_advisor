import pytest
from core.build_simulator import BuildSimulator

def test_build_with_real_price(monkeypatch):
    # Mock da TradeClient para não bater na API real
    def mock_fetch_prices(self, payload, limit=1):
        return [{"type": "Iron Ring", "price": 7, "currency": "chaos"}]

    monkeypatch.setattr("core.trade_client.TradeClient.fetch_prices", mock_fetch_prices)

    build = BuildSimulator()
    build.add_ring_with_real_price()

    assert build.total_build_cost() == 7
    summary = build.summary()
    assert "Iron Ring" in summary
    assert "TOTAL BUILD: 7c" in summary
