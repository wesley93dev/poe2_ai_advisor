from core.payload_builder import PayloadBuilder
from core.item_simulator import ItemSimulator

class BuildSimulator:
    """
    Integra PayloadBuilder e ItemSimulator.
    Permite simular builds completas com custo total.
    """

    def __init__(self):
        self.items = []

    def add_ring_with_chaos(self, chaos_cost: int = 5):
        """Adiciona um anel com Chaos Orb como mod."""
        payload = PayloadBuilder.for_rings_with_chaos()
        ring = ItemSimulator("Ring", base_cost=0)
        ring.add_mod("Chaos Orb implicit", chaos_cost)
        self.items.append((payload, ring))

    def total_build_cost(self) -> int:
        """Soma o custo de todos os itens da build."""
        return sum(item.total_cost() for _, item in self.items)

    def summary(self) -> str:
        """Resumo textual da build."""
        lines = [item.summary() for _, item in self.items]
        return "\n".join(lines) + f"\nTOTAL BUILD: {self.total_build_cost()}c"
