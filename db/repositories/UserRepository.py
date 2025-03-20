import db.Database as database
from db.entities.user import User
from exceptions.UserNotFoundException import UserNotFoundException

class UserRepository:

    def __init__(self):

        self._db = database.Database("bevolkingsregister.db")

    def get_by_username(self, username):

        user = self._db.fetch_one("SELECT * FROM users WHERE gebruikersnaam=?",(username,))

        if not user:
            raise UserNotFoundException(f"Gebruiker met gebruikersnaam {username} kan niet gevonden worden!")

        return User(user[0],user[1],user[2],user[3],user[4],user[5],user[6],user[7])

    def get_by_id(self, id:int):

        user = self._db.fetch_one("SELECT * FROM users WHERE id=?",(id,))

        if not user:
            raise UserNotFoundException(f"Gebruiker met id {id} kan niet gevonden worden!")

        return User(user[0],user[1],user[2],user[3],user[4],user[5],user[6],user[7])

    def get_user_count(self):
        return self._db.fetch_one("SELECT COUNT(id) FROM users")

    def create_user(self, username:str,password:str,rol:int):

        return self._db.insert("INSERT INTO users(gebruikersnaam,wachtwoord,rol) VALUES(?,?,?)",(username.lower(),password,rol,))

    def update_user(self, user:User):

        return self._db.update("UPDATE users SET wachtwoord=?,rol=? WHERE id=?", (user.password,user.role,user.id))