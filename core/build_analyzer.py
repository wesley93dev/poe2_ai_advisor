import requests
import re

class BuildAnalyzer:
    def __init__(self, profile_url):
        self.profile_url = profile_url

    def fetch_build(self):
        """Busca dados crus da build no poe.ninja"""
        resp = requests.get(self.profile_url)
        resp.raise_for_status()
        return resp.text

    def parse_stats(self, raw_data):
        """Extrai Chaos Resist, Evasion e DPS do HTML/JSON do poe.ninja"""
        stats = {}

        # Chaos Resist
        chaos_match = re.search(r"Resistances.*?(\d+)%\s+37%", raw_data)
        if chaos_match:
            stats["chaos_res"] = int(chaos_match.group(1))
        else:
            chaos_match = re.search(r"(\d+)%\s+37%", raw_data)
            stats["chaos_res"] = int(chaos_match.group(1)) if chaos_match else 0

        # Evasion
        evasion_match = re.search(r"Evasion rating\s+([\d,]+)", raw_data)
        stats["evasion"] = int(evasion_match.group(1).replace(",", "")) if evasion_match else 0

        # DPS (pega Ice Strike como skill principal)
        dps_match = re.search(r"Ice Strike\s+([\d,]+)k", raw_data)
        if dps_match:
            stats["dps"] = int(dps_match.group(1).replace(",", "")) * 1000
        else:
            stats["dps"] = 0

        return stats

    def detect_needs(self, stats):
        """Detecta gargalos com base nos valores extraídos"""
        needs = []

        if stats["chaos_res"] < 60:
            needs.append("Chaos Resist baixo")
        if stats["evasion"] < 20000:
            needs.append("Evasion pode melhorar")
        if stats["dps"] < 100000:
            needs.append("DPS baixo para tier atual")

        return needs
