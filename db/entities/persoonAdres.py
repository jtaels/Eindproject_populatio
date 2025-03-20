from db.entities.adres import Adres
from db.entities.persoon import Persoon

class PersoonAdres:

    def __init__(self, id, persoon:Persoon, adres:Adres, adres_type, van, tot):
        self.id = id
        self.persoon = persoon
        self.adres = adres
        self.adres_type = adres_type
        self.van = van
        self.tot = tot