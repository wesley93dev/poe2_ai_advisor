import requests

class TradeClient:
    """
    Cliente simples para consultar a API do PoE2 Trade.
    """

    BASE_URL = "https://www.pathofexile.com/api/trade2"

    def __init__(self, league: str = "Rise of the Abyssal"):
        self.league = league

    def search_item(self, query_payload: dict) -> list:
        """
        Faz uma busca no PoE2 Trade e retorna os resultados.
        """
        url = f"{self.BASE_URL}/search/poe2/{self.league}"
        response = requests.post(url, json=query_payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data

    def fetch_prices(self, query_payload: dict, limit: int = 5) -> list:
        """
        Retorna os preços dos primeiros itens encontrados.
        """
        data = self.search_item(query_payload)
        if "result" not in data or not data["result"]:
            return []

        # IDs dos primeiros resultados
        ids = data["result"][:limit]
        fetch_url = f"{self.BASE_URL}/fetch/{','.join(ids)}?query={data['id']}"
        response = requests.get(fetch_url, timeout=15)
        response.raise_for_status()
        items = response.json().get("result", [])
        return [
            {
                "name": item.get("item", {}).get("name"),
                "type": item.get("item", {}).get("typeLine"),
                "price": item.get("listing", {}).get("price", {}).get("amount"),
                "currency": item.get("listing", {}).get("price", {}).get("currency"),
            }
            for item in items
        ]
