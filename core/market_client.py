import requests

class MarketClient:
    def __init__(self, league, session_cookie):
        self.league = league
        self.session_cookie = session_cookie
        self.base_url = f"https://www.pathofexile.com/api/trade2/search/poe2/{league}"

    def search(self, payload):
        headers = {
            "Cookie": self.session_cookie,
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Referer": f"https://www.pathofexile.com/trade2/search/poe2/{self.league}"
        }
        resp = requests.post(self.base_url, json=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()
