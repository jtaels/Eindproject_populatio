import db.Database as database
from db.entities.gemeente import Gemeente
from db.repositories.AdresRepository import AdresRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from db.repositories.GemeenteRepository import GemeenteRepository
from db.entities.persoon import Persoon
from exceptions.GemeenteNotFound import GemeenteNotFoundException
from exceptions.PersonCreateFailure import PersonCreateFailureException
from exceptions.PersonNotFound import PersonNotFoundException
from exceptions.PersonUpdateFailure import PersonUpdateFailureException
from datetime import datetime

class PersoonRepository:

    def __init__(self,gemeente_repository:GemeenteRepository):

        self._db = database.Database("bevolkingsregister.db")
        self._gemeente_repository = gemeente_repository
        self._adres_repository = AdresRepository(self._gemeente_repository)
        self._persoon_adres_repository = PersoonAdresRepository(self._adres_repository, self)

    def find_by_id(self,id:int) -> Persoon:

        result = self._db.fetch_one("SELECT * FROM personen WHERE id=?", (id,))

        if not result:
            raise PersonNotFoundException(f"Persoon met id {id} bestaat niet!")

        person = self._build_entity(result)

        return self._fill_adresses(person)

    def find_by_bevolkingsregisternr(self,bevolkingsregisternr:str) -> Persoon:

        result = self._db.fetch_one("SELECT * FROM personen WHERE bevolkingsregisternummer=?", (bevolkingsregisternr,))

        if not result:
            raise PersonNotFoundException(f"Persoon met id {id} bestaat niet!")

        person = self._build_entity(result)

        return self._fill_adresses(person)

    def find_by_name(self, firstname:str,lastname) -> list:

        persons = []

        results = self._db.fetch_all("SELECT * FROM personen WHERE voornaam LIKE ? AND achternaam LIKE ?", (f"%{firstname}%",f"%{lastname}%",))

        for result in results:

            try:

                person = self._build_entity(result)
                self._fill_adresses(person)

                persons.append(person)

            except PersonNotFoundException:
                continue

        return persons

    def create_person(self, person:Persoon) -> Persoon:

        last_id = self._db.insert("""
        
            INSERT INTO personen(
            
                voornaam,
                achternaam,
                geboortedatum,
                geboorteplaats_id,
                overlijdensdatum,
                overlijdensplaats_id,
                overlijdensoorzaak,
                bevolkingsregisternummer
            
            )
            
            VALUES(
            
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?
            
            )
        
        """,
    (
            person.voornaam,
            person.achternaam,
            person.geboortedatum,
            person.geboorteplaats.id if person.geboorteplaats else None,
            person.overlijdensdatum,
            person.overlijdensplaats.id if person.overlijdensplaats else None,
            person.overlijdensoorzaak,
            person.bevolkingsregisternummer,
            )

        )

        if last_id == 0:
            raise PersonCreateFailureException()

        person.id = last_id

        return person

    def update(self, person: Persoon) -> Persoon:

        rows_affected = self._db.update("""
            UPDATE personen
            SET
                voornaam = ?,
                achternaam = ?,
                geboortedatum = ?,
                geboorteplaats_id = ?,
                overlijdensdatum = ?,
                overlijdensplaats_id = ?,
                overlijdensoorzaak = ?
            WHERE id = ?
        """, (
            person.voornaam,
            person.achternaam,
            person.geboortedatum.strftime("%d-%m-%Y") if person.geboortedatum else None,
            person.geboorteplaats.id if person.geboorteplaats else None,
            person.overlijdensdatum.strftime("%d-%m-%Y") if person.overlijdensdatum else None,
            person.overlijdensplaats.id if person.overlijdensplaats else None,
            person.overlijdensoorzaak,
            person.id  # ID van de persoon die geüpdatet moet worden
        ))

        # Controleer of er daadwerkelijk rijen zijn bijgewerkt
        if rows_affected == 0:
            raise PersonUpdateFailureException()

        return person

    #Adressen in de entity opbouwen
    def _fill_adresses(self, person:Persoon) ->Persoon:

        adresses = self._persoon_adres_repository.find_by_person(person)
        person.set_adressen(adresses)

        return person

    def _get_geboorteplaats_and_overlijdensplaats(self, geboorteplaats_id, overlijdensplaats_id):

        def get_gemeente(gemeente_id):
            try:
                return self._gemeente_repository.get_by_id(gemeente_id)
            except GemeenteNotFoundException as e:
                print("[DEBUG]" + e.message)
                return None

        return get_gemeente(geboorteplaats_id), get_gemeente(overlijdensplaats_id)

    #Entity vanuit database opbouwen
    def _build_entity(self, result) -> Persoon:

        if not result:
            raise PersonNotFoundException()

        geboorteplaats,overlijdensplaats = self._get_geboorteplaats_and_overlijdensplaats(result[4],result[6])

        return Persoon(

            result[0], #id
            result[1], #voornaam
            result[2], #achternaam
            datetime.strptime(result[3], "%d-%m-%Y") if result[3] and result[3] != '' else None, #geboortedatum
            geboorteplaats, #geboorteplaats
            datetime.strptime(result[5],"%d-%m-%Y") if result[5] and result[5] != '' else None, #overlijdensdatum
            overlijdensplaats, #overlijdensplaats
            result[7], #overlijdensoorzaak
            result[8], #bevolkingsregisternummer

        )
