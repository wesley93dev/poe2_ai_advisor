from core.build_analyzer import BuildAnalyzer
from core.market_client import MarketClient
from core.payload_builder import PayloadBuilder
from core.item_simulator import ItemSimulator
from core.notifier import Notifier
from core.meta_advisor import MetaAdvisor

class Advisor:
    def __init__(self, build_url, league, session_cookie, current_res, webhook_url=None):
        self.analyzer = BuildAnalyzer(build_url)
        self.market = MarketClient(league, session_cookie)
        self.builder = PayloadBuilder(league)
        self.simulator = ItemSimulator(current_res)
        self.current_res = current_res
        self.notifier = Notifier(webhook_url) if webhook_url else None

    def run(self):
        """Executa análise da build + busca no mercado"""
        raw_build = self.analyzer.fetch_build()
        stats = self.analyzer.parse_stats(raw_build)
        needs = self.analyzer.detect_needs(stats)

        recommendations = []

        for need in needs:
            if "Chaos Resist" in need:
                payload = self.builder.for_chaos_res()
                results = self.market.search(payload)
                recommendations.extend(self.evaluate_items(results, "Chaos Resist"))

            if "Evasion" in need:
                payload = self.builder.for_evasion()
                results = self.market.search(payload)
                recommendations.extend(self.evaluate_items(results, "Evasion"))

            if "DPS" in need:
                payload = self.builder.for_dps_weapon("staff")
                results = self.market.search(payload)
                recommendations.extend(self.evaluate_items(results, "DPS"))

        # --- Meta Advisor (gems e flasks) ---
        your_gems = ["Ice Strike", "Rapid Attacks", "Crescendo", "Elemental Armament", "Pinpoint Critical"]
        meta_gems = ["Ice Strike", "Rapid Attacks", "Crescendo", "Elemental Armament", "Pinpoint Critical", "Rage"]

        your_flasks = ["Life Flask", "Mana Flask"]
        meta_flasks = ["Jade Flask", "Quartz Flask"]

        meta = MetaAdvisor(your_gems, your_flasks, meta_gems, meta_flasks)
        missing_gems = meta.compare_gems()
        missing_flasks = meta.compare_flasks()

        # Retorna tudo para o runner controlar duplicados
        return {
            "recommendations": recommendations,
            "missing_gems": missing_gems,
            "missing_flasks": missing_flasks
        }

    def evaluate_items(self, results, focus):
        """Avalia e ranqueia os itens"""
        scored_items = []
        for item_id in results.get("result", [])[:10]:
            item = results["listing"].get(item_id, {})
            mods = self.extract_resistances(item)

            # Mock: resistências do item atual (depois puxamos do inventário real)
            item_current = {"fire": 30, "cold": 20, "lightning": 25, "chaos": 0}
            new_res, valid = self.simulator.simulate_swap(item_current, mods)

            if valid:
                price = self.extract_price(item)
                gain = self.calculate_gain(new_res, focus)
                score = gain / max(price, 1)
                trade_link = f"https://www.pathofexile.com/trade2/search/poe2/{self.market.league}/{item_id}"
                scored_items.append({
                    "id": item_id,
                    "res": new_res,
                    "price": price,
                    "gain": gain,
                    "score": score,
                    "focus": focus,
                    "link": trade_link
                })
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        return scored_items

    def extract_resistances(self, item):
        """Extrai resistências do JSON do trade"""
        mods = {"fire": 0, "cold": 0, "lightning": 0, "chaos": 0}
        if "mods" in item:
            for mod in item["mods"]:
                text = mod.get("text", "").lower()
                if "fire resistance" in text:
                    mods["fire"] += int("".join([c for c in text if c.isdigit()]))
                if "cold resistance" in text:
                    mods["cold"] += int("".join([c for c in text if c.isdigit()]))
                if "lightning resistance" in text:
                    mods["lightning"] += int("".join([c for c in text if c.isdigit()]))
                if "chaos resistance" in text:
                    mods["chaos"] += int("".join([c for c in text if c.isdigit()]))
        return mods

    def extract_price(self, item):
        """Extrai preço do item"""
        try:
            return int(item.get("price", {}).get("amount", 9999))
        except:
            return 9999

    def calculate_gain(self, new_res, focus):
        """Calcula ganho percentual baseado no foco"""
        if focus == "Chaos Resist":
            return new_res["chaos"] - self.current_res["chaos"]
        elif focus == "Evasion":
            return (new_res.get("evasion", 0) - 17404) / 174.04  # % ganho
        elif focus == "DPS":
            return 20  # placeholder, depois calculamos DPS real
        return 0
