import json

class GemeenteLoader:
    def __init__(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_gemeenten = json.load(f)

        # Voeg een id toe aan elke gemeente op basis van index (startend bij 1)
        self.gemeenten = [
            {**g, "id": idx + 1} for idx, g in enumerate(raw_gemeenten)
        ]

    def get_gemeente_by_id(self, gemeente_id):
        return next((g for g in self.gemeenten if g['id'] == gemeente_id), None)

    def get_random_gemeente(self):
        import random
        return random.choice(self.gemeenten)

    def get_gemeenten(self):

        return self.gemeenten