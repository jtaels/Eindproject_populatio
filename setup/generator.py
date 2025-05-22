from faker import Faker

from Container import Container
from db.entities.adres import Adres
from db.entities.gemeente import Gemeente
from setup.adres_generator import AdresGenerator
from setup.gemeente_loader import GemeenteLoader
from setup.person_generator import PersonGenerator


class Generator:
    def __init__(self, gemeente_filepath, container:Container):
        self.fake = Faker('nl_BE')
        self.container = container
        self.gemeente_loader = GemeenteLoader(gemeente_filepath)
        self.adres_generator = AdresGenerator(self.gemeente_loader)
        self.person_generator = PersonGenerator(self.gemeente_loader)

    def run(self):

        self.insert_gemeente_db()
        self.insert_straten_db()
        self.insert_personen()

    def insert_gemeente_db(self):

        gemeente_service = self.container.get('gemeente_service')

        for gemeenteData in self.gemeente_loader.get_gemeenten():

            gemeente_service.create(Gemeente(None,gemeenteData['gemeente'],gemeenteData['postcode'],gemeenteData['provincie']))

    def insert_straten_db(self):

        adres_service = self.container.get('adres_service')

        for i in range(260):

            adres = self.adres_generator.genereer_adres()

            adres_service.create(Adres(None,adres['straatnaam'],adres['huisnummer'],adres['busnummer'], Gemeente(adres['gemeente_id'],adres['gemeente_naam'],adres['postcode'],None),[]))

    def insert_personen(self):

        persoon_service = self.container.get('persoon_service')

        for i in range(1000):
            persoon = self.person_generator.generate_person()

            persoon_service.create(
                persoon['voornaam'],
                persoon['achternaam'],
                persoon['geboortedatum'],
                Gemeente(persoon['gemeente_id'], None,None,None),
                '',
                None,
            "")
