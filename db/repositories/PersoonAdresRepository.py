import db.Database as database
from db.entities.adres import Adres
from db.entities.persoon import Persoon
from db.entities.persoonAdres import PersoonAdres
from exceptions.AdresNotFound import AdresNotFoundException
from exceptions.PersonAddAddressFailure import PersonAddAddressFailure
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

    def delete_person_from_address(self,person_address_id:int):

        return self._db.delete("DELETE FROM persoonAdressen WHERE id=?", (person_address_id,))

    def add_person_to_address(self, person_id:int,address_id:int) -> int:

        last_id = self._db.insert("INSERT INTO persoonAdressen(persoon_id,adres_id,adres_type) VALUES(?,?,'Hoofdverblijf')", (person_id,address_id))

        if last_id == 0:
            raise PersonAddAddressFailure

        return last_id

    def person_is_in_address(self, person_id:int,address_id:int) -> bool:

        result = self._db.fetch_one("SELECT id FROM persoonAdressen WHERE persoon_id=? AND adres_id=?", (person_id,address_id,))

        return result is not None

    def _build_entity(self, result, persoon:Persoon,adres:Adres):

        return PersoonAdres(result[0],persoon,adres,result[2],result[3],result[4])