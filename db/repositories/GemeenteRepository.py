import db.Database as database
from db.entities.gemeente import Gemeente
from exceptions.CreateGemeenteFailed import CreateGemeenteFailed
from exceptions.GemeenteNotFound import GemeenteNotFoundException

class GemeenteRepository:

    def __init__(self):

        self._db = database.Database("bevolkingsregister.db")

    def get_by_id(self, id:int) -> Gemeente:

        result = self._db.fetch_one("SELECT * FROM gemeenten WHERE id=?", (id,))

        return self._build_entity(result)

    def get_by_name(self, name: str) -> Gemeente:

        result = self._db.fetch_one("SELECT * FROM gemeenten WHERE naam=?", (name,))

        return self._build_entity(result)

    def get_by_zipcode(self, zipcode:str) -> Gemeente:

        result = self._db.fetch_one("SELECT * FROM gemeente WHERE postcode=?", (id,zipcode))

        return self._build_entity(result)

    def get_all_by_province(self, province:str) -> list:

        gemeenten = []

        results = self._db.fetch_all("SELECT * FROM gemeente WHERE postcode=?", (id,province))

        for result in results:
            gemeenten.append(self._build_entity(result))

        return gemeenten

    def update(self,gemeente:Gemeente) -> int:

        return self._db.update("UPDATE gemeenten SET naam=?,postcode=?,provincie=? WHERE id=?",(gemeente.naam,gemeente.postcode,gemeente.provincie,gemeente.id))

    def create(self, gemeente:Gemeente) -> Gemeente:

        last_row_id = self._db.insert("INSERT INTO gemeenten(naam,postcode,provincie) VALUES(?,?,?)")

        if last_row_id > 0:

            gemeente.id = last_row_id

            return gemeente

        raise CreateGemeenteFailed()


    '''
    Entity opbouwen vanuit de database
    '''
    def _build_entity(self,result) -> Gemeente:

        if not result:
            raise GemeenteNotFoundException()

        if len(result) != 4:
            raise ValueError(f"Ongeldig database resultaat: verwacht 4 kolommen, maar kreeg er {len(result)}.")

        return Gemeente(result[0],result[1],result[2],result[3])