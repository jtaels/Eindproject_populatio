import db.Database as database
from db.entities.adres import Adres
from db.entities.gemeente import Gemeente
from db.repositories.GemeenteRepository import GemeenteRepository
from exceptions.AdresNotFound import AdresNotFoundException
import sqlite3

class AdresRepository:

    def __init__(self, gemeenteRepository:GemeenteRepository):

        self._db = database.Database("bevolkingsregister.db")

    '''
    
    Adres zoeken. Gemeente moet altijd meegegeven worden zodat het moeilijker word te enumeraten.
    
    '''
    def find(self,straatnaam:str,huisnummer:str,busnummer:str,gemeente:Gemeente):

        adressen = []

        params = (straatnaam,huisnummer,busnummer,gemeente.id,)
        results = self._db.fetch_all("SELECT * FROM adressen WHERE straatnaam=? AND huisnummer=? AND busnummer=? AND gemeente_id=?",params)

        for result in results:

            adressen.append(self._build_entity(result,gemeente))

        return adressen

    def find_all_by_gemeente(self, gemeente:Gemeente):

        adressen = []

        params = (gemeente.id,)
        results = self._db.fetch_all(
            "SELECT * FROM adressen WHERE gemeente_id=?", params)

        for result in results:
            adressen.append(self._build_entity(result, gemeente))

        return adressen

    def find_by_id(self, id:int) -> Adres:

        result = self._db.fetch_one("""SELECT a.id as adresId,
                                              a.straatnaam,
                                              a.huisnummer,
                                              a.busnummer,
                                              g.id as gemeenteId,
                                              g.naam,
                                              g.postcode,
                                              g.provincie
                                              FROM adressen a
                                              JOIN gemeenten g ON g.id = a.gemeente_id
                                              WHERE a.id = ?""", (id,))
        if not result:
            raise AdresNotFoundException

        gemeente = Gemeente(result[4],result[5],result[6],result[7])

        return self._build_entity(result,gemeente)

    def delete(self, id:int) -> int:

        try:

            rows_affected = self._db.delete("DELETE FROM adressen WHERE id=?", (id,))

            return rows_affected

        except sqlite3.IntegrityError as e:
            raise e

    def create(self, adres:Adres) -> Adres:

        try:

            last_id = self._db.insert("INSERT INTO adressen(straatnaam,huisnummer,busnummer,gemeente_id) VALUES(?,?,?,?)", (adres.straatnaam,adres.huisnummer,adres.busnummer,adres.gemeente.id))

            adres.id = last_id

            return adres

        except sqlite3.IntegrityError as e:
            raise e

    def _build_entity(self, result,gemeente:Gemeente) -> Adres:

        if not result:
            raise AdresNotFoundException()

        return Adres(result[0],result[1],result[2],result[3], gemeente, [])