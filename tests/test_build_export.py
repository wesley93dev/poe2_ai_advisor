from core.build_simulator import BuildSimulator

def test_export_json_and_markdown(monkeypatch):
    # Mock para não bater na API real
    def mock_fetch_prices(self, payload, limit=1):
        return [{"type": "Iron Ring", "price": 10, "currency": "chaos"}]

    monkeypatch.setattr("core.trade_client.TradeClient.fetch_prices", mock_fetch_prices)

    build = BuildSimulator()
    build.add_ring_with_real_price()

    json_output = build.to_json()
    md_output = build.to_markdown()

    assert "Iron Ring" in json_output
    assert "Iron Ring" in md_output
    assert "TOTAL BUILD COST" in md_output
