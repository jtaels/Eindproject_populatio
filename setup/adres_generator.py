import random

class AdresGenerator:
    def __init__(self, gemeente_loader):
        self.gemeente_loader = gemeente_loader
        self.straatnamen = self._genereer_unieke_straatnamen()

    def _genereer_unieke_straatnamen(self):
        prefixes = [
            "Kerk", "Station", "School", "Dorp", "Markt", "Sint-Jan", "Boom", "Molen",
            "Berg", "Linde", "Industrie", "Deurne", "Water", "H.-Hart", "Bos", "Zuid",
            "Noord", "Oost", "West", "Kapel", "Mechel", "Gent", "Brugge", "Antwerps",
            "Sport", "Veld", "Hoog", "Lage", "Kleine", "Grote", "Kleine", "Velo","Diester", "Molse", "Nieuwedijk", "Geelse", "Antwerpse"
        ]

        suffixes = ["straat", "laan", "weg", "dreef", "baan", "lei", "steenweg"]

        straatnamen = [f"{p}{s}" for p in prefixes for s in suffixes]
        random.shuffle(straatnamen)
        return straatnamen

    def genereer_adres(self):
        gemeente = self.gemeente_loader.get_random_gemeente()

        straatnaam = self.straatnamen.pop() if self.straatnamen else f"Straat{random.randint(1000,9999)}"
        huisnummer = random.randint(1, 200)
        busnummer = random.choice(["", "A", "B", "bis"])

        return {
            "straatnaam": straatnaam,
            "huisnummer": huisnummer,
            "busnummer": busnummer,
            "gemeente_id": gemeente["id"],
            "gemeente_naam": gemeente["gemeente"],
            "postcode": gemeente["postcode"]
        }
