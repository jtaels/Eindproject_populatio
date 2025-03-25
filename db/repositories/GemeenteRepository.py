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

        result = self._db.fetch_one("SELECT * FROM gemeenten WHERE postcode=?", (id,zipcode))

        return self._build_entity(result)

    def get_all_by_province(self, province:str) -> list:

        gemeenten = []

        results = self._db.fetch_all("SELECT * FROM gemeenten WHERE provincie=?", (province,))

        for result in results:
            gemeenten.append(self._build_entity(result))

        return gemeenten

    def get_all(self) -> list:

        gemeenten = []

        results = self._db.fetch_all("SELECT * FROM gemeenten")

        for result in results:
            gemeenten.append(self._build_entity(result))

        return gemeenten

    def update(self,gemeente:Gemeente) -> int:

        return self._db.update("UPDATE gemeenten SET naam=?,postcode=?,provincie=? WHERE id=?",(gemeente.naam,gemeente.postcode,gemeente.provincie,gemeente.id))

    def create(self, gemeente:Gemeente) -> Gemeente:

        last_row_id = self._db.insert("INSERT INTO gemeenten(naam,postcode,provincie) VALUES(?,?,?)", (gemeente.naam,gemeente.postcode,gemeente.provincie))

        if last_row_id > 0:

            gemeente.id = last_row_id

            return gemeente

        raise CreateGemeenteFailed()

    def delete(self, id:int) -> int:

        return self._db.delete("DELETE FROM gemeenten WHERE id=?", (id,))


    '''
    Entity opbouwen vanuit de database
    '''
    def _build_entity(self,result) -> Gemeente:

        if not result:
            raise GemeenteNotFoundException()

        if len(result) != 4:
            raise ValueError(f"Ongeldig database resultaat: verwacht 4 kolommen, maar kreeg er {len(result)}.")

        return Gemeente(result[0],result[1],result[2],result[3])