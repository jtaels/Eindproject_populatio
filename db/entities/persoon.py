class Persoon:
    def __init__(self, id:int, voornaam:str, achternaam:str, geboortedatum:str, geboorteplaats, overlijdensdatum:str, overlijdensplaats, overlijdensoorzaak:str, bevolkingsregisternummer:str):
        self.id = id
        self.voornaam = voornaam
        self.achternaam = achternaam
        self.geboortedatum = geboortedatum
        self.geboorteplaats = geboorteplaats
        self.overlijdensdatum = overlijdensdatum
        self.overlijdensplaats = overlijdensplaats
        self.overlijdensoorzaak = overlijdensoorzaak
        self.bevolkingsregisternummer = bevolkingsregisternummer
        self.adressen = []

    def set_adressen(self, adressen):
        self.adressen = adressen