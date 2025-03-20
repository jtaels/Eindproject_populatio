import db.Database as database
from db.entities.persoon import Persoon

class PersoonRepository:

    def __init__(self,persoon_adres_repository):

        self._db = database.Database("bevolkingsregister.db")
        self._persoon_adres_repository : persoon_adres_repository

    def find_by_id(self,id:int):
        pass

    def find_by_name(self, firstname:str,lastname):
        pass