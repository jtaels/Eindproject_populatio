from db.entities.adres import Adres
from db.entities.gemeente import Gemeente
from db.repositories.AdresRepository import AdresRepository
from db.repositories.PersoonAdresRepository import PersoonAdresRepository
from exceptions.AdresNotFound import AdresNotFoundException


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