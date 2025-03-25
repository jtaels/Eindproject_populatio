from db.entities.gemeente import Gemeente
from services.GemeenteService import GemeenteService


class GemeenteManager:

    def __init__(self, gemeente_service:GemeenteService):

        self._gemeente_service = gemeente_service
        self.reload_gemeenten()

    def get_gemeente_by_name(self, name: str) -> Gemeente | None:

        return self._gemeente_dict.get(name)

    def reload_gemeenten(self):
        self._gemeenten = self._gemeente_service.find_all()
        self._gemeente_dict = {g.naam: g for g in self._gemeenten}