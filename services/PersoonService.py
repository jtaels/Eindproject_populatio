from db.entities.gemeente import Gemeente
from db.entities.persoon import Persoon
from db.repositories.PersoonRepository import PersoonRepository
from exceptions.FormErrorException import FormErrorException
from exceptions.PersonCreateFailure import PersonCreateFailureException
from exceptions.PersonNotFound import PersonNotFoundException
from exceptions.PersonUpdateFailure import PersonUpdateFailureException
from validator.PersonFormValidator import PersonFormValidator
import random
from datetime import datetime

class PersoonService:

    def __init__(self, persoon_repository:PersoonRepository):

        self._person_repository = persoon_repository

    def get_person_by_id(self, id:int) -> Persoon:

        try:

            return self._person_repository.find_by_id(id)

        except PersonNotFoundException as e:
            raise e

    def search_by_name(self, firstname: str, lastname: str) -> list:

        return self._person_repository.find_by_name(firstname, lastname)

    def create(self, firstname:str,lastname:str,birthdate:str,birtplace:Gemeente,deathdate:str,deathplace:Gemeente,overlijdensoorzaak:str) -> Persoon:

        validator = PersonFormValidator(firstname,lastname, birthdate,deathdate)

        validator.validate()

        errors, has_errors = validator.get_errors()

        if has_errors:
            raise FormErrorException(errors)

        persoon = Persoon(

            0,
            firstname,
            lastname,
            birthdate,
            birtplace,
            deathdate,
            deathplace,
            overlijdensoorzaak,
            self._generate_bevolkingsregisterNr(birthdate)

        )

        try:
            return self._person_repository.create_person(persoon)
        except PersonCreateFailureException as e:
            raise e

    def _generate_bevolkingsregisterNr(self,geboortedatum):

        geboortedatum_obj = datetime.strptime(geboortedatum, "%Y-%m-%d")


        dag = geboortedatum_obj.day
        maand = geboortedatum_obj.month
        jaar = geboortedatum_obj.year % 100


        volgnummer = random.randint(100, 999)
        checknummer = random.randint(10, 99)

        # Maak het bevolkingsnummer
        bevolkingsnummer = f"{dag:02d}{maand:02d}{jaar:02d}-{volgnummer}-{checknummer}"

        return bevolkingsnummer

    def update_persoon(self, person: Persoon) -> Persoon:

        validator = PersonFormValidator(person.voornaam, person.achternaam, person.geboortedatum, person.overlijdensdatum)

        validator.validate()

        errors, has_errors = validator.get_errors()


        if has_errors:
            raise FormErrorException(errors)

        try:
            return self._person_repository.update(person)
        except PersonUpdateFailureException as e:
            raise e