from db.entities.adres import Adres
from db.entities.gemeente import Gemeente
from db.entities.persoon import Persoon
from db.entities.persoonAdres import PersoonAdres
from db.repositories.AdresRepository import AdresRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from exceptions.AdresNotFound import AdresNotFoundException
from exceptions.PersonAddAddressFailure import PersonAddAddressFailure


class AdresService:

    def __init__(self, adres_repository:AdresRepository, person_address_repository:PersoonAdresRepository):

        self.adres_repository = adres_repository
        self.person_address_repository = person_address_repository

    def find_one(self,straatnaam:str,huisnummer:str,busnummer:str,gemeente:Gemeente) -> Adres:

        adres = self.adres_repository.find(straatnaam,huisnummer,busnummer,gemeente)

        if len(adres) == 0:
            raise AdresNotFoundException()

        adres = adres[0]

        inwoners = self.person_address_repository.find_by_adres(adres)

        adres.bewoners = inwoners

        return adres

    def create(self, adres:Adres):

        return self.adres_repository.create(adres)

    def get_address_details(self, persoon_id:int,adres_id:int) -> PersoonAdres:

        return self.person_address_repository.get_address_details(persoon_id,adres_id)

    def get_by_person(self,person:Persoon) -> list:

        return self.person_address_repository.find_by_person(person)

    def delete_person_from_address(self,person_address_id):

        return self.person_address_repository.delete_person_from_address(person_address_id)

    def add_person_to_address(self, person_id:int,address_id:int):

        return self.person_address_repository.add_person_to_address(person_id, address_id)

    def person_is_in_address(self,person_id:int,address_id:int) -> bool:

        return self.person_address_repository.person_is_in_address(person_id, address_id)