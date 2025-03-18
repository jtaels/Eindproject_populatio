import db.Database as database
import db.entities.user as UserEntity
from exceptions.UserNotFoundException import UserNotFoundException

class UserRepository:

    def __init__(self):

        self._db = database.Database("bevolkingsregister.db")

    def get_by_username(self, username):

        user = self._db.fetch_one("SELECT * FROM users WHERE gebruikersnaam=?",(username,))

        if not user:
            raise UserNotFoundException(f"Gebruiker met gebruikersnaam {username} kan niet gevonden worden!")

        return user

    def get_by_id(self, id:int):

        user = self._db.fetch_one("SELECT * FROM users WHERE id=?",(id,))

        if not user:
            raise UserNotFoundException(f"Gebruiker met id {id} kan niet gevonden worden!")

        return user

    def get_user_count(self):
        return self._db.fetch_one("SELECT COUNT(id) FROM users")

    def create_user(self, username:str,password:str,rol:int):

        return self._db.insert("INSERT INTO users(gebruikersnaam,wachtwoord,rol) VALUES(?,?,?)",(username,password,rol,))