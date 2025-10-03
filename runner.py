import time
from core.advisor import Advisor

if __name__ == "__main__":
    BUILD_URL = "https://poe.ninja/poe2/profile/alkaida11-5703/character/Abyss_SubZero"
    LEAGUE = "Rise of the Abyssal"
    SESSION_COOKIE = "POESESSID=..."  # seu cookie válido
    CURRENT_RES = {"fire": 75, "cold": 75, "lightning": 76, "chaos": 37}
    WEBHOOK_URL = "https://discord.com/api/webhooks/XXXX/XXXX"

    advisor = Advisor(BUILD_URL, LEAGUE, SESSION_COOKIE, CURRENT_RES, WEBHOOK_URL)

    seen_items = set()

    while True:
        print("🔄 Checando mercado...")
        result = advisor.run()
        new_recs = result["recommendations"]

        for rec in new_recs:
            if rec["id"] not in seen_items:
                advisor.notifier.send_message(
                    f"⚡ Novo upgrade encontrado ({rec['focus']}) ⚡\n"
                    f"💰 Preço: {rec['price']} Divine\n"
                    f"📈 Ganho: {rec['gain']}%\n"
                    f"🏆 Score: {rec['score']:.2f}\n"
                    f"🛡 Resistências finais: "
                    f"F:{rec['res']['fire']} C:{rec['res']['cold']} "
                    f"L:{rec['res']['lightning']} Ch:{rec['res']['chaos']}\n"
                    f"🔗 [Abrir no Trade]({rec['link']})"
                )
                seen_items.add(rec["id"])

        # Gems e Flasks sugeridos
        if result["missing_gems"] or result["missing_flasks"]:
            summary = ""
            if result["missing_gems"]:
                summary += f"💎 Gems sugeridas: {', '.join(result['missing_gems'])}\n"
            if result["missing_flasks"]:
                summary += f"🥤 Flasks sugeridos: {', '.join(result['missing_flasks'])}\n"
            advisor.notifier.send_message(summary)

        time.sleep(60)  # checa a cada 1 minuto
