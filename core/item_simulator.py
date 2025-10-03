class ItemSimulator:
    def __init__(self, current_res):
        """
        current_res: dict com resistências totais atuais
        Exemplo:
        {
            "fire": 75,
            "cold": 75,
            "lightning": 75,
            "chaos": 37
        }
        """
        self.current_res = current_res

    def simulate_swap(self, item_current, item_candidate):
        """
        item_current: resistências fornecidas pelo item atual
        item_candidate: resistências fornecidas pelo novo item
        Exemplo:
        item_current = {"fire": 30, "cold": 20, "lightning": 25, "chaos": 0}
        item_candidate = {"fire": 0, "cold": 34, "lightning": 39, "chaos": 24}
        """
        # Remove resistências do item atual
        new_res = {
            ele: self.current_res.get(ele, 0) - item_current.get(ele, 0)
            for ele in ["fire", "cold", "lightning", "chaos"]
        }

        # Adiciona resistências do item candidato
        for ele in ["fire", "cold", "lightning", "chaos"]:
            new_res[ele] += item_candidate.get(ele, 0)

        # Validação
        valid = (
            new_res["fire"] >= 75 and
            new_res["cold"] >= 75 and
            new_res["lightning"] >= 75 and
            new_res["chaos"] >= self.current_res["chaos"]
        )

        return new_res, valid
