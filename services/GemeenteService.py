from db.repositories.GemeenteRepository import GemeenteRepository


class GemeenteService:

    def __init__(self, gemeente_repository:GemeenteRepository):

        self._gemeente_repository = gemeente_repository

    def find_all(self):

        return self._gemeente_repository.get_all()