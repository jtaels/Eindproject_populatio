from db.entities.gemeente import Gemeente
from services.GemeenteService import GemeenteService


class GemeenteManager:

    def __init__(self, gemeente_service:GemeenteService):

        self._gemeente_service = gemeente_service
        self.reload_gemeenten()

        self.gemeente_dict = {}
        self.postcode_dict = {}

        self.reload_gemeenten()

    def get_gemeente_by_name(self, name: str) -> Gemeente | None:

        return self.gemeente_dict.get(name)

    def get_gemeente_by_postcode(self, postcode: str) -> Gemeente | None:

        return self.postcode_dict.get(postcode)

    def reload_gemeenten(self):
        self._gemeenten = self._gemeente_service.find_all()
        # Sorteren op naam
        self._gemeenten.sort(key=lambda g: g.naam.lower())
        self.gemeente_dict = {g.naam: g for g in self._gemeenten}
        self.postcode_dict = {g.postcode: g for g in self._gemeenten}
