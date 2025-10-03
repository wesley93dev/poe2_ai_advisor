class CurrencyConverter:
    """
    Conversor simples de moedas do PoE2 para Chaos Orbs.
    Taxas podem ser ajustadas conforme o mercado.
    """

    RATES_TO_CHAOS = {
        "chaos": 1,
        "divine": 180,   # Exemplo: 1 Divine = 180 Chaos
        "exalted": 50,   # Exemplo: 1 Exalted = 50 Chaos
    }

    @classmethod
    def to_chaos(cls, amount: float, currency: str) -> float:
        currency = currency.lower()
        if currency not in cls.RATES_TO_CHAOS:
            raise ValueError(f"Moeda não suportada: {currency}")
        return amount * cls.RATES_TO_CHAOS[currency]
