from core.payload_builder import PayloadBuilder
from core.item_simulator import ItemSimulator
from core.trade_client import TradeClient

class BuildSimulator:
    """
    Integra PayloadBuilder, ItemSimulator e TradeClient.
    Permite simular builds completas com custo real.
    """

    def __init__(self, league: str = "Rise of the Abyssal"):
        self.items = []
        self.client = TradeClient(league=league)

    def add_ring_with_real_price(self):
        """Adiciona um anel com Chaos Orb implícito, usando preço real do mercado."""
        payload = PayloadBuilder.for_rings_with_chaos()
        prices = self.client.fetch_prices(payload, limit=1)

        if not prices:
            # fallback se não encontrar nada
            ring = ItemSimulator("Ring", base_cost=0)
            ring.add_mod("Chaos Orb implicit", 5)
        else:
            price_info = prices[0]
            amount = price_info.get("price", 0)
            currency = price_info.get("currency", "chaos")
            ring = ItemSimulator(price_info.get("type", "Ring"), base_cost=0)
            ring.add_mod(f"Chaos Orb implicit [{currency}]", amount)

        self.items.append(ring)

    def total_build_cost(self) -> int:
        """Soma o custo de todos os itens da build (em Chaos)."""
        return sum(item.total_cost() for item in self.items)

    def summary(self) -> str:
        """Resumo textual da build."""
        lines = [item.summary() for item in self.items]
        return "\n".join(lines) + f"\nTOTAL BUILD: {self.total_build_cost()}c"
