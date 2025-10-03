from core.payload_builder import PayloadBuilder
from core.item_simulator import ItemSimulator
from core.trade_client import TradeClient
from core.currency_converter import CurrencyConverter

class BuildSimulator:
    def __init__(self, league: str = "Rise of the Abyssal"):
        self.items = []
        self.client = TradeClient(league=league)

    def add_ring_with_real_price(self):
        payload = PayloadBuilder.for_rings_with_chaos()
        prices = self.client.fetch_prices(payload, limit=1)

        if not prices:
            ring = ItemSimulator("Ring", base_cost=0)
            ring.add_mod("Chaos Orb implicit", 5)
        else:
            price_info = prices[0]
            amount = price_info.get("price", 0)
            currency = price_info.get("currency", "chaos")
            chaos_value = CurrencyConverter.to_chaos(amount, currency)

            ring = ItemSimulator(price_info.get("type", "Ring"), base_cost=0)
            ring.add_mod(f"Chaos Orb implicit [{currency}]", chaos_value)

        self.items.append(ring)

    def total_build_cost(self) -> int:
        return sum(item.total_cost() for item in self.items)

    def summary(self) -> str:
        lines = [item.summary() for item in self.items]
        return "\n".join(lines) + f"\nTOTAL BUILD: {self.total_build_cost()}c"
