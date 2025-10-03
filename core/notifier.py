import requests

class Notifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, content):
        requests.post(self.webhook_url, json={"content": content})


    def send(self, item_id, price, gain, score, new_res, focus, trade_link):
        """Envia notificação para o Discord"""
        message = {
            "content": (
                f"⚡ **Upgrade encontrado ({focus})** ⚡\n"
                f"🔹 Item ID: `{item_id}`\n"
                f"💰 Preço: {price} Divine\n"
                f"📈 Ganho estimado: {gain}%\n"
                f"🏆 Score: {score:.2f}\n"
                f"🛡 Resistências finais: "
                f"F:{new_res['fire']} C:{new_res['cold']} L:{new_res['lightning']} Ch:{new_res['chaos']}\n"
                f"🔗 [Abrir no Trade]({trade_link})"
            )
        }
        requests.post(self.webhook_url, json=message)
