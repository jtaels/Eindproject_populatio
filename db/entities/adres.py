from db.entities.gemeente import Gemeente
from db.entities.persoon import Persoon

class Adres:

    def __init__(self, id, straatnaam:str, huisnummer:str, busnummer:str,gemeente:Gemeente,personen:list):
        self.id = id
        self.straatnaam = straatnaam
        self.huisnummer = huisnummer
        self.busnummer = busnummer
        self.gemeente = gemeente
        self.bewoners = personen