class PayloadBuilder:
    def __init__(self, league):
        self.league = league

    def for_chaos_res(self):
        return {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {"filters": {"category": {"option": "armour.chest"}}},
                    "misc_filters": {"filters": {"chaos_resistance": {"min": 20}}}
                }
            },
            "sort": {"price": "asc"}
        }

    def for_evasion(self):
        return {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {"filters": {"category": {"option": "armour.chest"}}},
                    "armour_filters": {"filters": {"evasion": {"min": 2500}}}
                }
            },
            "sort": {"price": "asc"}
        }

    def for_dps_weapon(self, weapon_type):
        return {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {"filters": {"category": {"option": f"weapon.{weapon_type}"}}},
                    "weapon_filters": {"filters": {"dps": {"min": 40000}}}
                }
            },
            "sort": {"price": "asc"}
        }

    # 🚀 Novo módulo sugerido pela IA
    def for_rings_with_chaos(self):
        return {
            "query": {
                "status": {"option": "online"},
                "filters": {
                    "type_filters": {"filters": {"category": {"option": "accessory.ring"}}},
                    "misc_filters": {"filters": {"chaos_resistance": {"min": 20}}}
                }
            },
            "sort": {"price": "asc"}
        }
