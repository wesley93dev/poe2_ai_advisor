import pytest
from core.payload_builder import PayloadBuilder

def test_for_rings_with_chaos():
    builder = PayloadBuilder("Rise of the Abyssal")
    payload = builder.for_rings_with_chaos()

    # Categoria deve ser anel
    assert payload["query"]["filters"]["type_filters"]["filters"]["category"]["option"] == "accessory.ring"

    # Deve exigir pelo menos 20% de resistência ao caos
    assert payload["query"]["filters"]["misc_filters"]["filters"]["chaos_resistance"]["min"] == 20

    # Ordenação deve ser por preço ascendente
    assert payload["sort"]["price"] == "asc"
