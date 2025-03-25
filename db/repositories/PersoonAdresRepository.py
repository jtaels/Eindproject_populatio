import db.Database as database
from db.entities.adres import Adres
from db.entities.persoon import Persoon
from db.entities.persoonAdres import PersoonAdres
from exceptions.AdresNotFound import AdresNotFoundException
from exceptions.PersonNotFound import PersonNotFoundException


class PersoonAdresRepository:

    def __init__(self,adres_repository:'AdresRepository',persoon_repository:'PersoonRepository'):

        self._db = database.Database("bevolkingsregister.db")

        self._adres_repository = adres_repository
        self._persoon_repository = persoon_repository

    def find_by_adres(self, adres:Adres):

        personen = []

        results = self._db.fetch_all("SELECT id,persoon_id,adres_type,van,tot FROM persoonAdressen WHERE adres_id=?",
                                     (adres.id,))

        for result in results:

            #Indien persoon niet gevonden word slaan we deze over
            try:

                persoon = self._persoon_repository.find_by_id(result[1])

            except PersonNotFoundException as e:
                continue

            persoon_adres = self._build_entity(result, persoon, adres)

            personen.append(persoon_adres)

        return personen

    def find_by_person(self,persoon:Persoon):

        adressen = []

        results = self._db.fetch_all("SELECT id,adres_id,adres_type,van,tot FROM persoonAdressen WHERE persoon_id=?", (persoon.id,))

        for result in results:

            # Indien adres niet gevonden word slaan we deze over
            try:

                adres = self._adres_repository.find_by_id(result[1])

            except AdresNotFoundException as e:

                continue

            persoon_adres = self._build_entity(result,persoon,adres)

            adressen.append(persoon_adres)

        return adressen

    def _build_entity(self, result, persoon:Persoon,adres:Adres):

        return PersoonAdres(result[0],persoon,adres,result[2],result[3],result[4])